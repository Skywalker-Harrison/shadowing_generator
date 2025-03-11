#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from parse_srt import parse_srt_by_sentence, save_sentences_to_file, save_sentences_to_json

def main():
    """Test the functionality of parse_srt.py"""
    # Specify SRT file path
    srt_file_path = "video.srt"
    output_srt = "sentences.srt"
    output_json = "sentences.json"
    
    try:
        # Parse SRT file, split by sentences
        print(f"Parsing SRT file: {srt_file_path}")
        sentences = parse_srt_by_sentence(srt_file_path)
        
        # Print the number of sentences found
        print(f"Found {len(sentences)} sentences")
        
        # Print information for the first 5 sentences
        print("\nInformation for the first 5 sentences:")
        for i, sentence in enumerate(sentences[:5]):
            print(f"Sentence {i+1}:")
            print(f"  Text: {sentence['text']}")
            print(f"  Start time: {sentence['start_formatted']}")
            print(f"  End time: {sentence['end_formatted']}")
            print()
        
        # Save sentences to SRT file
        save_sentences_to_file(sentences, output_srt)
        print(f"Sentences have been saved to SRT file: {output_srt}")
        
        # Save sentences to JSON file
        save_sentences_to_json(sentences, output_json)
        print(f"Sentences have been saved to JSON file: {output_json}")
        
        print("\nNow you can run the following command to generate a shadow reading video:")
        print(f"python generate_video.py --video video.mp4 --json {output_json} --output output.mp4")
        print("\nOr run the GUI interface directly:")
        print("python generate_video.py")
        
    except Exception as e:
        print(f"Error during testing: {str(e)}")

if __name__ == "__main__":
    main() 