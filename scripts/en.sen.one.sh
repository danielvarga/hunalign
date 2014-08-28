huntoken -e -b | grep "\(^<s>\)\|\(^  <p>\)" | sed "s/^<s>//" | sed "s/^  <p>/<p>/"
