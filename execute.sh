#! bin/bash
time for file in inputs/*; 
    do python3 hoteleiro.py ${file%.txt} $((600 - SECONDS)) < $file; 
done
