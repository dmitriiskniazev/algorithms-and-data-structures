cmake_minimum_required(VERSION 4.4)

if(CMAKE_VERSION VERSION_LESS 4.5)
    set(CMAKE_EXPERIMENTAL_CXX_IMPORT_STD "f35a9ac6-8463-4d38-8eec-5d6008153e7d")
endif()

if(NOT CMAKE_GENERATOR MATCHES "Ninja")
    message(FATAL_ERROR "The C++ course uses the Ninja generator.")
endif()

if(NOT CMAKE_CXX_COMPILER)
    if(DEFINED ENV{CXX})
        set(CMAKE_CXX_COMPILER "$ENV{CXX}" CACHE FILEPATH "C++ compiler")
    else()
        find_program(CMAKE_CXX_COMPILER NAMES clang++ REQUIRED)
    endif()
endif()

if(NOT CMAKE_CXX_STDLIB_MODULES_JSON)
    execute_process(
        COMMAND "${CMAKE_CXX_COMPILER}" -print-file-name=libc++.modules.json
        OUTPUT_VARIABLE LIBCXX_MODULES_JSON
        OUTPUT_STRIP_TRAILING_WHITESPACE
        ERROR_QUIET
    )
    if(NOT IS_ABSOLUTE "${LIBCXX_MODULES_JSON}" OR NOT EXISTS "${LIBCXX_MODULES_JSON}")
        get_filename_component(CXX_COMPILER_REALPATH "${CMAKE_CXX_COMPILER}" REALPATH)
        get_filename_component(CXX_COMPILER_DIRECTORY "${CXX_COMPILER_REALPATH}" DIRECTORY)
        get_filename_component(CXX_COMPILER_PREFIX "${CXX_COMPILER_DIRECTORY}" DIRECTORY)
        unset(LIBCXX_MODULES_JSON CACHE)
        unset(LIBCXX_MODULES_JSON)
        find_file(
            LIBCXX_MODULES_JSON
            NAMES libc++.modules.json
            HINTS
                "${CXX_COMPILER_PREFIX}/lib/c++"
                "${CXX_COMPILER_PREFIX}/share/libc++/v1"
                "${CXX_COMPILER_PREFIX}/share/libc++"
        )
    endif()
    if(NOT LIBCXX_MODULES_JSON)
        message(FATAL_ERROR
            "Could not locate libc++.modules.json. Set CMAKE_CXX_STDLIB_MODULES_JSON to its path."
        )
    endif()
    set(CMAKE_CXX_STDLIB_MODULES_JSON "${LIBCXX_MODULES_JSON}" CACHE FILEPATH
        "Metadata describing the libc++ standard modules")
endif()

project(algorithms_and_data_structures LANGUAGES CXX)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON CACHE BOOL "Export compile commands" FORCE)

set(CMAKE_CXX_STANDARD 26)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
set(CMAKE_CXX_MODULE_STD ON)

if(NOT CMAKE_CXX_COMPILER_ID MATCHES "Clang")
    message(FATAL_ERROR "The C++ course requires Clang with C++26 support.")
endif()
if(CMAKE_CXX_COMPILER_VERSION VERSION_LESS 23)
    message(FATAL_ERROR "The C++ course requires Clang 23 or newer.")
endif()

enable_testing()

add_library(sorting_algorithms)
target_sources(sorting_algorithms
    PUBLIC
        FILE_SET CXX_MODULES FILES
            impl/cpp/src/algorithms/sorting/bubble_sort/bubble_sort.cppm
            impl/cpp/src/algorithms/sorting/insertion_sort/insertion_sort.cppm
            impl/cpp/src/algorithms/sorting/selection_sort/selection_sort.cppm
            impl/cpp/src/algorithms/sorting/sorting.cppm
)

foreach(ALGORITHM IN ITEMS bubble_sort insertion_sort selection_sort)
    add_executable(test_${ALGORITHM}
        impl/cpp/tests/algorithms/sorting/${ALGORITHM}/test_${ALGORITHM}.cpp
    )
    target_link_libraries(test_${ALGORITHM} PRIVATE sorting_algorithms)
    add_test(NAME ${ALGORITHM} COMMAND test_${ALGORITHM})
endforeach()
