#include "common.hpp"
#include <libgen.h>

void debug_log(char *fn, char *s, ...) {
    va_list ap;
    va_start(ap, s);
    char *filename = strdup(fn);
    filename = basename(filename);
    char *log_filename = (char *)malloc(strlen(filename) + 5);
    strcpy(log_filename, filename);
    strcat(log_filename, ".log");
    FILE *fp = fopen(log_filename, "a");
    vfprintf(fp, s, ap);
    va_end(ap);
    fclose(fp);
}

