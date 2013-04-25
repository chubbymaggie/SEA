#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>
#include <fcntl.h>
#include <string.h>
#include <ctype.h>
#include <stdarg.h>
#include <errno.h>
#include <sys/socket.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <netinet/in.h>

enum { use_fork = 0 };

static FILE *cur_f;	/* connection being currently handled */

static int
fgets_trim(char *buf, int size, FILE *f)
{
    char *p = fgets(buf, size, f);
    if (!p)
	return -1;

    /* Trim newline characters at the end of the line */
    while (buf[strlen(buf) - 1] == '\r' ||
	   buf[strlen(buf) - 1] == '\n')
    buf[strlen(buf) - 1] = '\0';

    return 0;
}

static void
url_decode(char *src, char *dst)
{
    for (;;) {
	if (src[0] == '%' && src[1] && src[2]) {
	    char hexbuf[3];
	    hexbuf[0] = src[1];
	    hexbuf[1] = src[2];
	    hexbuf[2] = '\0';

	    *dst = strtol(&hexbuf[0], 0, 16);
	    src += 3;
	} else {
	    *dst = *src;
	    src++;

	    if (*dst == '\0')
		break;
	}

	dst++;
    }
}

static char *
parse_req(char *reqpath)
{
    static char buf[8192];	/* static variables are not on the stack */

    if (fgets_trim(&buf[0], sizeof(buf), cur_f) < 0)
	return "Socket IO error";

    /* Parse request like "GET /foo.html HTTP/1.0" */
    char *sp1 = strchr(&buf[0], ' ');
    if (!sp1)
	return "Cannot parse HTTP request (1)";
    *sp1 = '\0';
    sp1++;

    char *sp2 = strchr(sp1, ' ');
    if (!sp2)
	return "Cannot parse HTTP request (2)";
    *sp2 = '\0';
    sp2++;

    /* We only support GET requests */
    if (strcmp(&buf[0], "GET"))
	return "Non-GET request";

    /* Decode URL escape sequences in the requested path into reqpath */
    url_decode(sp1, reqpath);

    /* Parse out query string, e.g. "foo.py?user=bob" */
    char *qp = strchr(reqpath, '?');
    if (qp) {
	*qp = '\0';
	setenv("QUERY_STRING", qp+1, 1);
    }

    /* Now parse HTTP headers */
    for (;;) {
	if (fgets_trim(&buf[0], sizeof(buf), cur_f) < 0)
	    return "Socket IO error";

	if (buf[0] == '\0')	/* end of headers */
	    break;

	/* Parse things like "Cookie: foo bar" */
	char *sp = strchr(&buf[0], ' ');
	if (!sp)
	    return "Header parse error (1)";
	*sp = '\0';
	sp++;

	/* Strip off the colon, making sure it's there */
	if (strlen(buf) == 0)
	    return "Header parse error (2)";

	char *colon = &buf[strlen(buf) - 1];
	if (*colon != ':')
	    return "Header parse error (3)";
	*colon = '\0';

	/* Set the header name to uppercase */
	for (int i = 0; i < strlen(buf); i++)
	    buf[i] = toupper(buf[i]);

	/* Decode URL escape sequences in the value */
	char value[256];
	url_decode(sp, &value[0]);

	/* Store header in env. variable for application code */
	char envvar[256];
	sprintf(&envvar[0], "HTTP_%s", buf);
	setenv(envvar, value, 1);
    }

    return 0;
}

static void
http_err(FILE *f, int code, char *fmt, ...)
{
    va_list ap;
    va_start(ap, fmt);

    fprintf(f, "HTTP/1.0 %d Error\r\n", code);
    fprintf(f, "Content-Type: text/html\r\n");
    fprintf(f, "\r\n");
    fprintf(f, "<H1>An error occurred</H1>\r\n");
    vfprintf(f, fmt, ap);

    va_end(ap);
    fclose(f);
}

static void
process_client(const char *dir, int fd)
{
    char reqpath[256];
    FILE *f = fdopen(fd, "w+");
    cur_f = f;

    char *err = parse_req(&reqpath[0]);
    if (err) {
	http_err(f, 500, "Error parsing request: %s", err);
	return;
    }

    char pn[1024];
    sprintf(&pn[0], "%s/%s", dir, reqpath);
    struct stat st;
    if (stat(pn, &st) < 0) {
	http_err(f, 404, "File not found or not accessible: %s", pn);
	return;
    }

    if (S_ISDIR(st.st_mode)) {
	/* For directories, use index.html in that directory */
	strcat(pn, "/index.html");
	if (stat(pn, &st) < 0) {
	    http_err(f, 404, "File not found or not accessible: %s", pn);
	    return;
	}
    }

    if (S_ISREG(st.st_mode) && (st.st_mode & S_IXUSR)) {
	/* executable bits -- run as CGI script */
	fflush(f);

	signal(SIGCHLD, SIG_DFL);
	int pid = fork();
	if (pid < 0) {
	    http_err(f, 500, "Cannot fork: %s", strerror(errno));
	    return;
	}

	if (pid == 0) {
	    /* Child process */
	    int nullfd = open("/dev/null", O_RDONLY);
	    dup2(nullfd, 0);
	    dup2(fileno(f), 1);
	    dup2(fileno(f), 2);

	    close(nullfd);
	    fclose(f);

	    execl(pn, pn, 0);
	    perror("execl");
	    exit(-1);
	}

	int status;
	waitpid(pid, &status, 0);
	fclose(f);
    } else {
	/* Non-executable: serve contents */
	int fd = open(pn, O_RDONLY);
	if (fd < 0) {
	    http_err(f, 500, "Cannot open %s: %s", pn, strerror(errno));
	    return;
	}

	fprintf(f, "HTTP/1.0 200 OK\r\n");
	fprintf(f, "Content-Type: text/html\r\n");
	fprintf(f, "\r\n");

	for (;;) {
	    char readbuf[1024];
	    int cc = read(fd, &readbuf[0], sizeof(readbuf));
	    if (cc <= 0)
		break;

	    fwrite(&readbuf[0], 1, cc, f);
	}

	close(fd);
	fclose(f);
    }
}

int
main(int ac, const char **av)
{
    if (ac != 3) {
	fprintf(stderr, "Usage: %s port dir\n", av[0]);
	exit(-1);
    }

    int port = atoi(av[1]);
    const char *dir = av[2];

    if (!port) {
	fprintf(stderr, "Bad port number: %s\n", av[1]);
	exit(-1);
    }

    struct sockaddr_in sin;
    sin.sin_family = AF_INET;
    sin.sin_addr.s_addr = INADDR_ANY;
    sin.sin_port = htons(port);

    int srvfd = socket(AF_INET, SOCK_STREAM, 0);
    if (srvfd < 0) {
	perror("socket");
	exit(-1);
    }

    int on = 1;
    if (setsockopt(srvfd, SOL_SOCKET, SO_REUSEADDR, &on, sizeof(on)) < 0) {
	perror("setsockopt SO_REUSEADDR");
	exit(-1);
    }

    if (bind(srvfd, (struct sockaddr *) &sin, sizeof(sin)) < 0) {
	perror("bind");
	exit(-1);
    }

    listen(srvfd, 5);
    signal(SIGCHLD, SIG_IGN);
    signal(SIGPIPE, SIG_IGN);

    for (;;) {
	struct sockaddr_in client_addr;
	unsigned int addrlen = sizeof(client_addr);

	int cfd = accept(srvfd, (struct sockaddr *) &client_addr, &addrlen);
	if (cfd < 0) {
	    perror("accept");
	    continue;
	}

	int pid = use_fork ? fork() : 0;
	if (pid < 0) {
	    perror("fork");
	    close(cfd);
	    continue;
	}

	if (pid == 0) {
	    /* Child process. */
	    if (use_fork)
		close(srvfd);

	    process_client(dir, cfd);

	    if (use_fork)
		exit(0);
	}

	if (pid > 0) {
	    /* Parent process. */
	    close(cfd);
	}
    }
}
