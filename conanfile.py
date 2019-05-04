#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os
import shutil


class v8Conan(ConanFile):
    name = "v8"
    version = "2019.01"
    description = "Javascript Engine"
    topics = ("javascript", "C++", "embedded", "google")
    url = "https://github.com/inexorgame/conan-v8"
    homepage = "https://v8.dev"
    author = "a_teammate <madoe3@web.de>"
    license = "MIT"  # Indicates license type of the packaged library; please use SPDX Identifiers https://spdx.org/licenses/
    # exports = ["COPYING"]
    # exports_sources = ["BUILD.gn", "DEPS", "*", "!.git/*"]
    # exports_sources = ["CMakeLists.txt", "src/*", "!src/*/*/Test", "package/conan/*", "modules/*"]
    generators = "cmake"
    # short_paths = True  # Some folders go out of the 260 chars path length scope (windows)

    settings = "os", "arch", "compiler", "build_type"
    

    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    build_requires = "depot_tools_installer/master@bincrafters/stable"

    def system_requirements(self):
        # Install required OpenGL stuff on linux
        packages = []
        """
        if tools.os_info.is_linux:
            if tools.os_info.with_apt:
                installer = tools.SystemPackageTool()
                packages.append("libgl1-mesa-dev")
            else:
                self.output.warn("Could not determine package manager, skipping Linux system requirements installation.")

        for package in packages:
            installer.install("{}{}".format(package, arch_suffix))
        """

    def configure(self):
        """
        self.options['corrade'].add_option('build_deprecated', self.options.build_deprecated)

        # To fix issue with resource management, see here:
        # https://github.com/mosra/magnum/issues/304#issuecomment-451768389
        if self.options.shared:
            self.options['corrade'].add_option('shared', True)
        """

    def build_requirements(self):
        return
        # tools.download(
        '''
        if tools.os_info.is_linux:
            self.build_requires("bison/3.0.4@bincrafters/stable")
            self.build_requires("bzip2/1.0.6@conan/testing")
            self.build_requires("flex/2.6.4@bincrafters/stable")
            self.build_requires("OpenSSL/1.1.0g@conan/stable")
        '''

    def requirements(self):
        return

        if tools.os_info.is_linux:
            self.requires("libuuid/1.0.3@bincrafters/stable")
            self.requires("OpenSSL/1.1.0g@conan/stable")

    def source(self):
        
        # Set up depot_tools
        self.run("git clone https://chromium.googlesource.com/chromium/tools/depot_tools.git")
        new_path = "PATH=$PATH:`pwd`/depot_tools "
        # new_path = ""
        self.run(new_path + "gclient")
        self.run(new_path + "fetch v8")


    def build(self):
        new_path = "PATH=$PATH:`pwd`/depot_tools "
        # new_path = ""
        if tools.os_info.is_linux:
          self.run("chmod +x v8/build/install-build-deps.sh")
          self.run(new_path + "v8/build/install-build-deps.sh --unsupported")
        cmd = new_path + "cd v8 && tools/dev/v8gen.py x64.{build_type} -- v8_monolithic=true v8_static_library=true v8_use_external_startup_data=false is_component_build=false is_clang=false use_sysroot=false v8_enable_i18n_support=false v8_enable_backtrace=false use_glib=false use_custom_libcxx=false use_custom_libcxx_for_host = false treat_warnings_as_errors = false && ninja -C out.gn/x64.{build_type} v8_monolith".format(build_type=str(self.settings.build_type).lower())
        self.run(cmd)

    def package(self):
        self.copy(pattern="LICENSE*", dst="licenses", src="v8")
        self.copy(pattern="*v8_monolith.a", dst="lib", keep_paths=False)
        self.copy(pattern="*v8_monolith.lib", dst="lib", keep_paths=False)
        self.copy(pattern="*.h", dst="include", src="v8/include", keep_paths=True)
        

    def package_info(self):
        # fix issue on Windows and OSx not finding the KHR files
        # self.cpp_info.includedirs.append(os.path.join("include", "MagnumExternal", "OpenGL"))
        # builtLibs = tools.collect_libs(self)
        self.cpp_info.libs = ["v8_monolith"]  # sort_libs(correct_order=allLibs, libs=builtLibs, lib_suffix=suffix, reverse_result=True)

