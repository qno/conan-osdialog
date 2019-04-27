#include <osdialog.h>
#include <string>

int main() {

   std::string str = osdialog_strndup("Hello", 5);

   /** Parses a filter string.
    Example: "Source:c,cpp,m;Header:h,hpp"
    Caller must eventually free with osdialog_filters_free().
    osdialog_filters *osdialog_filters_parse(const char *str);
    void osdialog_filters_free(osdialog_filters *filters);
   */
   std::string filterStr = "Source:c,cpp,m;Header:h,hpp";
   auto* dialogFilters = osdialog_filters_parse(filterStr.c_str());

   // this opens a dialog windows and can't be used in a automated test
   // std::string path{"tmp"};
   // std::string file{"test"};
   // auto* dialogFile = osdialog_file(OSDIALOG_OPEN, path.c_str(), file.c_str(), dialogFilters);

   osdialog_filters_free(dialogFilters);

   return 0;
}
