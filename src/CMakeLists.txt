cmake_minimum_required(VERSION 3.5.0)
project(hunalign)

set(NAME hunalign)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)
set(CMAKE_CXX_FLAGS "-Wall -O9 -Ofast -ffast-math -funroll-loops")

include_directories(${PROJECT_SOURCE_DIR}/include)

set(sources hunalign/alignerTool.cpp hunalign/alignment.cpp hunalign/bloom.cpp hunalign/bookToMatrix.cpp hunalign/cooccurrence.cpp hunalign/cooccurrenceTool.cpp hunalign/dictionary.cpp hunalign/main.cpp hunalign/networkFlow.cpp hunalign/oldAlignTest.cpp hunalign/trailPostprocessors.cpp hunalign/translate.cpp hunalign/wordAlignment.cpp utils/stringsAndStreams.cpp utils/argumentsParser.cpp utils/timer.cpp)

set(headers hunalign/alignment.h hunalign/bloom.h hunalign/bookToMatrix.h hunalign/cooccurrence.h hunalign/dictionary.h hunalign/dicTree.h hunalign/help.h hunalign/networkFlow.h hunalign/quasiDiagonal.h hunalign/similarityEvaluator.h hunalign/TEIReader.h hunalign/trailPostprocessors.h hunalign/translate.h hunalign/wordAlignment.h hunalign/words.h)

add_library(hunalign_lib STATIC ${headers} ${sources})

add_executable(hunalign hunalign/main.cpp)
target_link_libraries(hunalign hunalign_lib)

install(TARGETS hunalign DESTINATION ${CMAKE_INSTALL_BINDIR})
