from conans import ConanFile, CMake, tools
from conans.client.tools.pkg_config import PkgConfig
from conans.errors import ConanInvalidConfiguration
import os

class OSDialogConan(ConanFile):
    name = "OSDialog"
    version = "master"
    license = "CC0"
    author = "Andrew Belt"
    url = "https://github.com/qno/conan-osdialog"
    description = "A cross platform wrapper for OS dialogs like file save, open, message boxes, inputs, color picking, etc."

    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    options = {"shared": [True, False]}
    default_options = "shared=False"

    _pkg_name = "osdialog-master"
    _libname = "osdialog"

    def source(self):
        url = "https://github.com/AndrewBelt/osdialog/archive/master.zip"
        self.output.info("Downloading {}".format(url))
        tools.get(url)
        self._createCMakeLists()

    def configure(self):
        if self._isVisualStudioBuild() and self.options.shared:
            raise ConanInvalidConfiguration("This library doesn't support dll's on Windows")

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_dir=self._pkg_name)
        cmake.build()

    def package(self):
        self.copy("*.h", dst="include", src=self._pkg_name)
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="lib", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = [self._libname]

        if self.settings.os == "Linux":
            pkg_config = PkgConfig("gtk+-2.0")
            for lib in pkg_config.libs_only_l:
                self.cpp_info.libs.append(lib[2:])


    def _isVisualStudioBuild(self):
        return self.settings.os == "Windows" and self.settings.compiler == "Visual Studio"

    def _createCMakeLists(self):
        content = '''\
# THIS FILE WAS GENERATED BY CONAN RECIPE. DO NOT EDIT THIS FILE!
cmake_minimum_required(VERSION 3.5)
project(OSDialog)

set (CMAKE_C_STANDARD 11)

include(${{CMAKE_BINARY_DIR}}/conanbuildinfo.cmake)
conan_basic_setup()

set(LIBOSDIALOG "{}")

if (CMAKE_SYSTEM_NAME STREQUAL "Windows")
   set(PLATFORM_SOURCE osdialog_win.c)
elseif (CMAKE_SYSTEM_NAME STREQUAL "Linux")
   set(PLATFORM_SOURCE osdialog_gtk2.c)
elseif (CMAKE_SYSTEM_NAME STREQUAL "Darwin")
   set(PLATFORM_SOURCE osdialog_mac.m)
else ()
   message(FATAL_ERROR "This platform '${{CMAKE_SYSTEM_NAME}}'is not supported by this library")
endif ()

set(SOURCES osdialog.c ${{PLATFORM_SOURCE}})

add_library(${{LIBOSDIALOG}} ${{SOURCES}})

if (CMAKE_SYSTEM_NAME STREQUAL "Linux")
   find_package(GTK2 REQUIRED)
   target_include_directories(${{LIBOSDIALOG}} PRIVATE ${{GTK2_INCLUDE_DIRS}})
   target_compile_definitions(${{LIBOSDIALOG}} PRIVATE GTK2_DEFINITIONS)
   target_link_libraries(${{LIBOSDIALOG}} PRIVATE ${{GTK2_LIBRARIES}})
endif ()

if (MSVC)
   target_compile_options(${{LIBOSDIALOG}} PRIVATE /Wall)
else ()
   target_compile_options(${{LIBOSDIALOG}} PRIVATE -Wall -Wextra -pedantic)
endif ()
'''.format(self._libname)

        self.output.info("create CMakeLists.txt file")
        cmake_file = os.path.join(self._pkg_name, "CMakeLists.txt")
        f = open(cmake_file, "w+")
        f.write(content)
        f.close()
