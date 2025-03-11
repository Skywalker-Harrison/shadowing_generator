#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import pysrt
import os
import json

def parse_srt_by_sentence(srt_file_path):
    """
    Parse SRT subtitle file, split content by sentences (periods), and get the timestamp for each sentence
    
    Args:
        srt_file_path: Path to the SRT file
        
    Returns:
        list: List of sentence information, each element is a dictionary containing sentence text, start time and end time
    """
    # Check if the file exists
    if not os.path.exists(srt_file_path):
        raise FileNotFoundError(f"SRT file does not exist: {srt_file_path}")
    
    # Load SRT file
    subtitles = pysrt.open(srt_file_path)
    
    # Merge all subtitle text while preserving time information
    merged_subtitles = []
    current_text = ""
    current_start = None
    current_end = None
    
    for sub in subtitles:
        # Get the current subtitle text and time
        text = sub.text.strip()
        start_time = (sub.start.hours * 3600 + 
                     sub.start.minutes * 60 + 
                     sub.start.seconds + 
                     sub.start.milliseconds / 1000)
        end_time = (sub.end.hours * 3600 + 
                   sub.end.minutes * 60 + 
                   sub.end.seconds + 
                   sub.end.milliseconds / 1000)
        
        # If the current subtitle ends with a period, question mark, or exclamation mark, it indicates the end of a sentence
        if re.search(r'[.!?]$', text) or not current_text:
            if not current_start:
                current_start = start_time
            current_text += " " + text if current_text else text
            current_end = end_time
            
            # If the sentence ends, add it to the merged list
            if re.search(r'[.!?]$', text):
                merged_subtitles.append({
                    'text': current_text.strip(),
                    'start': current_start,
                    'end': current_end
                })
                # Reset current sentence
                current_text = ""
                current_start = None
                current_end = None
        else:
            # If the current subtitle doesn't end with a period, continue accumulating text
            if not current_start:
                current_start = start_time
            current_text += " " + text if current_text else text
            current_end = end_time
    
    # Process the last unfinished sentence (if any)
    if current_text:
        merged_subtitles.append({
            'text': current_text.strip(),
            'start': current_start,
            'end': current_end
        })
    
    # Further process the merged subtitles, split by periods
    sentence_info = []
    
    for merged_sub in merged_subtitles:
        text = merged_sub['text']
        start_time = merged_sub['start']
        end_time = merged_sub['end']
        
        # Use regular expressions to split sentences
        # Match periods, question marks, or exclamation marks followed by spaces or end of string
        sentences = re.split(r'([.!?])\s*', text)
        
        # Reassemble sentences (because split will also split out the separators)
        complete_sentences = []
        i = 0
        while i < len(sentences):
            if i + 1 < len(sentences) and sentences[i+1] in ['.', '!', '?']:
                complete_sentences.append(sentences[i] + sentences[i+1])
                i += 2
            else:
                if sentences[i]:  # Ignore empty strings
                    complete_sentences.append(sentences[i])
                i += 1
        
        # Calculate the time ratio for each sentence
        if complete_sentences:
            time_per_sentence = (end_time - start_time) / len(complete_sentences)
            
            for i, sentence in enumerate(complete_sentences):
                sentence = sentence.strip()
                if not sentence:
                    continue
                
                # Calculate the start and end time of the sentence
                sentence_start = start_time + i * time_per_sentence
                sentence_end = sentence_start + time_per_sentence
                
                # Format time
                start_formatted = format_time(sentence_start)
                end_formatted = format_time(sentence_end)
                
                sentence_info.append({
                    'text': sentence,
                    'start': sentence_start,
                    'end': sentence_end,
                    'start_formatted': start_formatted,
                    'end_formatted': end_formatted
                })
    
    return sentence_info

def format_time(seconds):
    """
    Format seconds to HH:MM:SS,mmm format
    
    Args:
        seconds: Time in seconds
        
    Returns:
        str: Formatted time string
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = seconds % 60
    milliseconds = int((seconds - int(seconds)) * 1000)
    seconds = int(seconds)
    
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"

def save_sentences_to_file(sentences, output_file):
    """
    Save sentence information to a file
    
    Args:
        sentences: List of sentence information
        output_file: Output file path
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        for i, sentence in enumerate(sentences):
            f.write(f"{i+1}\n")
            f.write(f"{sentence['start_formatted']} --> {sentence['end_formatted']}\n")
            f.write(f"{sentence['text']}\n\n")

def save_sentences_to_json(sentences, output_file):
    """
    Save sentence information as a JSON file
    
    Args:
        sentences: List of sentence information
        output_file: Output JSON file path
    """
    # Create serializable data structure
    serializable_sentences = []
    for sentence in sentences:
        serializable_sentences.append({
            'text': sentence['text'],
            'start': sentence['start'],
            'end': sentence['end'],
            'start_formatted': sentence['start_formatted'],
            'end_formatted': sentence['end_formatted'],
            'repeat_count': 1  # Default repeat count is 1
        })
    
    # Save as JSON file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(serializable_sentences, f, ensure_ascii=False, indent=2)

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Split SRT file by sentences')
    parser.add_argument('--srt', required=True, help='Path to SRT file')
    parser.add_argument('--output', default='sentences.srt', help='Path to output SRT file')
    parser.add_argument('--json', default='sentences.json', help='Path to output JSON file')
    
    args = parser.parse_args()
    
    try:
        sentences = parse_srt_by_sentence(args.srt)
        
        # Save as SRT file
        save_sentences_to_file(sentences, args.output)
        print(f"Sentences have been saved to SRT file: {args.output}")
        
        # Save as JSON file
        save_sentences_to_json(sentences, args.json)
        print(f"Sentences have been saved to JSON file: {args.json}")
        
        print(f"Found {len(sentences)} sentences")
    except Exception as e:
        print(f"Error processing SRT file: {str(e)}")

if __name__ == "__main__":
    main() 