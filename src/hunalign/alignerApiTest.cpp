
#include <iostream>
#include <string>
#include "alignerApi.hpp"

using namespace std;
using namespace Hunalign;


auto readLinesFromFile(string filename) -> vector<string> {
    ifstream file(filename);
    vector<string> lines;
    string line;
    while (getline(file, line)) {
        lines.push_back(line);
    }
    return lines;
}

/* Add a main function that accepts three args: dict, src, tgt  runs aligner. This is a test case*/
int main(int argc, char* argv[]) {
    if (argc < 4) {
        // a minimal CLI for testing only
        std::cerr << "Usage: " << argv[0] << " <dictionary> <source> <target>" << std::endl;
        std::cerr << "Example: " << argv[0] << "  data/hu-en.stem.dic examples/demo.hu.stem examples/demo.en.stem" << std::endl;
        return 1;
    }
    string dictPath = argv[1];
    string srcPath = argv[2];
    string tgtPath = argv[3];

    AlignParameters alignParameters;
    HunAligner aligner(alignParameters, dictPath);

    cout << "====Aligning FIle API " << srcPath << " and " << tgtPath << "====\n";
    aligner.alignDocuments(srcPath, tgtPath);

    cout << "\n\n====Aligning In-Memory API " << srcPath << " and " << tgtPath << "====\n";
    // test the in-memory version
    vector<string> srcLines = readLinesFromFile(srcPath);
    vector<string> tgtLines = readLinesFromFile(tgtPath);
    auto [alignedLines, score] = aligner.alignDocuments(srcLines, tgtLines);
    for (auto& line : alignedLines) {
        cout << line << endl;
    }
    cout << "Quality score: " << score << endl;
    return 0;
}