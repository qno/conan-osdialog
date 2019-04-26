#include <osdialog.h>
#include <string>

int main() {

   char* pattern = "pattern";
   char* filter = "filter";
   osdialog_filter_patterns dialogPattern = {pattern, nullptr};
   osdialog_filters dialogFilter = {filter, &dialogPattern, nullptr};

   std::string str = osdialog_strndup("Hello", 5);

   /** Parses a filter string.
    Example: "Source:c,cpp,m;Header:h,hpp"
    Caller must eventually free with osdialog_filters_free().
    osdialog_filters *osdialog_filters_parse(const char *str);
    void osdialog_filters_free(osdialog_filters *filters);
   */
   std::string filterStr = "Source:c,cpp,m;Header:h,hpp";
   auto* dialogFilters = osdialog_filters_parse(filterStr.c_str());
   osdialog_filters_free(dialogFilters);

   // this opens a dialog windows and can't be used in a automated test
   // std::string path{"tmp"};
   // std::string file{"test"};
   // auto* dialogFile = osdialog_file(OSDIALOG_OPEN, path.c_str(), file.c_str(), &dialogFilter);

   return 0;
}
