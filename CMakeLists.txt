cmake_minimum_required(VERSION 3.10)


# Project name
project(hunalign)
# Set the C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Set the source and include directories
#set(SOURCE_DIR ${CMAKE_SOURCE_DIR}/src/hunalign)
set(INCLUDE_DIR ${CMAKE_SOURCE_DIR}/src/include)


# Set the C++ compiler
if (MSVC)
    set(CMAKE_CXX_COMPILER cl)
    # Set the compilation flags for MSVC
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /O2 /fp:fast /arch:AVX2")
    # 
    #  fatal  error C1189: #error:  <hash_map> is deprecated and will be REMOVED.
    add_definitions(-D_SILENCE_STDEXT_HASH_DEPRECATION_WARNINGS)
else()
    set(CMAKE_CXX_COMPILER g++)
    # Set the compilation flags for GCC
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -O9 -ffast-math -funroll-loops")
endif()

# Set the include directories
include_directories(${INCLUDE_DIR})

# Set the libraries to link against
if (MSVC)
    set(EXT_LIBS "")
else()
    set(EXT_LIBS -lstdc++)
endif()



# Collect all source files
#file(GLOB SOURCES "${SOURCE_DIR}/*.cpp")
set(SOURCES
    ${CMAKE_SOURCE_DIR}/src/hunalign/alignerTool.cpp
    ${CMAKE_SOURCE_DIR}/src/hunalign/alignment.cpp
    ${CMAKE_SOURCE_DIR}/src/hunalign/bloom.cpp
    ${CMAKE_SOURCE_DIR}/src/hunalign/bookToMatrix.cpp
    ${CMAKE_SOURCE_DIR}/src/hunalign/cooccurrence.cpp
    ${CMAKE_SOURCE_DIR}/src/hunalign/cooccurrenceTool.cpp
    ${CMAKE_SOURCE_DIR}/src/hunalign/dictionary.cpp
    ${CMAKE_SOURCE_DIR}/src/hunalign/main.cpp
    ${CMAKE_SOURCE_DIR}/src/hunalign/networkFlow.cpp
    ${CMAKE_SOURCE_DIR}/src/hunalign/oldAlignTest.cpp
    ${CMAKE_SOURCE_DIR}/src/hunalign/trailPostprocessors.cpp
    ${CMAKE_SOURCE_DIR}/src/hunalign/translate.cpp
    ${CMAKE_SOURCE_DIR}/src/hunalign/wordAlignment.cpp
    ${CMAKE_SOURCE_DIR}/src/utils/stringsAndStreams.cpp
    ${CMAKE_SOURCE_DIR}/src/utils/argumentsParser.cpp
    ${CMAKE_SOURCE_DIR}/src/utils/timer.cpp
    # new addition to the code
    ${CMAKE_SOURCE_DIR}/src/hunalign/alignerApi.hpp
)


# Add the library
add_library(hunalign STATIC ${SOURCES})
target_link_libraries(hunalign ${EXT_LIBS})

# executable: hunalign target is taken by the library,
# so hunalign_exe is the executable but the output file name should be hunalign instead of hunalign_exe
add_executable(hunalign_exe ${CMAKE_SOURCE_DIR}/src/hunalign/main.cpp)
set_property(TARGET hunalign_exe PROPERTY OUTPUT_NAME hunalign)

# Link the library to the executable
target_link_libraries(hunalign_exe PUBLIC hunalign ${EXT_LIBS})


# this is a test for using the simple API of the aligner
add_executable(hunalign_api_test ${CMAKE_SOURCE_DIR}/src/hunalign/alignerApiTest.cpp)
target_link_libraries(hunalign_api_test PUBLIC hunalign ${EXT_LIBS})

