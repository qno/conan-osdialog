#include <osdialog.h>

int main() {

   char* pattern = "pattern";
   char* filter = "filter";

   osdialog_filter_patterns dialogPattern = {pattern, nullptr};
   osdialog_filters dialogFilter = {filter, &dialogPattern, nullptr};

   return 0;
}
