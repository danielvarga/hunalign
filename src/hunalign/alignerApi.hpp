
#pragma once
#include <string>
#include <iostream>
#include <fstream>
#include <sstream>
#include <filesystem>
#include <tuple>
#include "./alignerTool.cpp"
#include "./dictionary.h"


using namespace std;
using namespace Hunglish;

namespace Hunalign {

    /**
     * @class HunAligner
     * @brief A class to handle alignment of documents using Hunalign.
     *
     * The HunAligner class provides functionality to align documents using the Hunalign tool.
     * It supports alignment using both file paths and in-memory strings.
     *
     * @note The dictionary file must exist at the specified path during initialization.
     */
    class HunAligner {
        protected:
            AlignParameters& alignParameters;
            string dictPath;
            DictionaryItems dictionary;

        public:
            /**
             * @brief Constructs a HunAligner object with the given alignment parameters and dictionary path.
             *
             * This constructor initializes the HunAligner with the provided alignment parameters and dictionary path.
             * It checks if the dictionary file exists at the specified path and reads the dictionary items from the file.
             *
             * @param alignParameters Reference to an AlignParameters object containing the alignment parameters.
             * @param dictPath Path to the dictionary file as a string.
             *
             * @throws std::invalid_argument if the dictionary file does not exist at the specified path.
             */
            HunAligner(AlignParameters& alignParameters, string dictPath)
            : alignParameters(alignParameters), dictPath(dictPath), dictionary(DictionaryItems()) {
                // check if the file exists
                if (!std::filesystem::exists(dictPath)) {
                    throw std::invalid_argument("Dictionary file does not exist: " + dictPath);
                }
                auto dictPathStream = std::ifstream (dictPath);
                dictionary.read(dictPathStream);
            }

            /**
             * @brief Aligns two documents and outputs the result.
             *
             * This method takes the filenames of two documents (source and target) and aligns them using the aligner tool.
             * The result can be optionally saved to an output file.
             *
             * @param srcFilename The filename of the source document.
             * @param tgtFilename The filename of the target document.
             * @param outPath The optional path to save the aligned output. If not provided, the result will be printed to STDOUT.
             */
            void alignDocuments(string srcFilename, string tgtFilename, string outPath="") {
                return alignerToolWithFilenames(
                    /*dictionary=*/this->dictionary,
                    /*huFilename=*/srcFilename,
                    /*enFilename=*/tgtFilename,
                    /*alignParameters=*/this->alignParameters,
                    /*outputFilename=*/outPath);
            }

        /**
         * @brief Aligns two sets of documents and returns the aligned result along with a quality score.
         *
         * This function takes two vectors of strings representing the source and target documents,
         * converts them into in-memory streams, and processes them to align the sentences. The alignment
         * is performed using the `alignerToolWithObjects` function, which utilizes a dictionary and
         * alignment parameters. The result is a tuple containing the aligned document as a vector of
         * strings and a double representing the global quality of the alignment.
         *
         * @param srcLines A vector of strings representing the source document lines.
         * @param tgtLines A vector of strings representing the target document lines.
         * @return A tuple containing:
         *         - A vector of strings (depends on the flags set in AlignParameters) representing the aligned document.
         *         - A double representing the global quality of the alignment.
         */
        tuple<vector<string>, double> alignDocuments(vector<string> srcLines, vector<string> tgtLines) {

            // convert vectors to in memory streams
            auto srcStream = std::stringstream();
            for (auto& line : srcLines) {
                srcStream << line << std::endl;
            }
            SentenceList huSentenceListPretty;
            huSentenceListPretty.readNoIds( srcStream );

            auto ens = std::stringstream();
            for (auto& line : tgtLines) {
                ens << line << std::endl;
            }
            SentenceList enSentenceList;
            enSentenceList.readNoIds( ens );

            auto outStream = std::ostringstream();
            double globalQuality = alignerToolWithObjects(
                dictionary,
                huSentenceListPretty,
                enSentenceList,
                alignParameters,
                outStream);
            auto outLines = std::vector<string>{outStream.str()};
            return make_tuple(std::move(outLines), globalQuality);
        }
    };

}