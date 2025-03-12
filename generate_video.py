#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import argparse
from moviepy.editor import VideoFileClip, concatenate_videoclips, TextClip, CompositeVideoClip, ColorClip
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

class SentenceEditor:
    """Sentence editor for editing the repeat count of each sentence"""
    def __init__(self, root, sentences, on_save):
        self.root = root
        self.sentences = sentences
        self.on_save = on_save
        
        self.root.title("Sentence Repeat Count Editor")
        self.root.geometry("800x600")
        
        # Create main frame
        main_frame = ttk.Frame(root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create batch settings frame
        batch_frame = ttk.LabelFrame(main_frame, text="Batch Settings", padding=10)
        batch_frame.pack(fill=tk.X, pady=10)
        
        # Batch settings controls
        ttk.Label(batch_frame, text="Set repeat count for all sentences:").grid(row=0, column=0, padx=5, pady=5)
        self.batch_repeat_var = tk.IntVar(value=2)
        batch_spinner = ttk.Spinbox(batch_frame, from_=1, to=10, textvariable=self.batch_repeat_var, width=5)
        batch_spinner.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(batch_frame, text="Apply", command=self.apply_batch).grid(row=0, column=2, padx=5, pady=5)
        
        # Subtitle display options
        ttk.Label(batch_frame, text="Show subtitles on which repeat:").grid(row=0, column=3, padx=5, pady=5)
        self.subtitle_display_var = tk.IntVar(value=2)  # Default to show subtitles on the second repeat
        subtitle_spinner = ttk.Spinbox(batch_frame, from_=0, to=10, textvariable=self.subtitle_display_var, width=5)
        subtitle_spinner.grid(row=0, column=4, padx=5, pady=5)
        ttk.Label(batch_frame, text="(0=All repeats, 1=First repeat, 2=Second repeat, ...)").grid(row=0, column=5, padx=5, pady=5)
        
        # Max characters per line for subtitles
        ttk.Label(batch_frame, text="Max characters per line:").grid(row=2, column=0, padx=5, pady=5)
        self.max_chars_var = tk.IntVar(value=40)  # Default to 40 characters per line
        max_chars_spinner = ttk.Spinbox(batch_frame, from_=20, to=80, textvariable=self.max_chars_var, width=5)
        max_chars_spinner.grid(row=2, column=1, padx=5, pady=5)
        ttk.Button(batch_frame, text="Apply", command=self.apply_batch).grid(row=2, column=2, padx=5, pady=5)
        
        # Create range settings
        ttk.Label(batch_frame, text="From sentence").grid(row=1, column=0, padx=5, pady=5)
        self.range_start_var = tk.IntVar(value=1)
        range_start_spinner = ttk.Spinbox(batch_frame, from_=1, to=len(sentences), textvariable=self.range_start_var, width=5)
        range_start_spinner.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(batch_frame, text="to sentence").grid(row=1, column=2, padx=5, pady=5)
        self.range_end_var = tk.IntVar(value=len(sentences))
        range_end_spinner = ttk.Spinbox(batch_frame, from_=1, to=len(sentences), textvariable=self.range_end_var, width=5)
        range_end_spinner.grid(row=1, column=3, padx=5, pady=5)
        
        ttk.Label(batch_frame, text="Repeat count:").grid(row=1, column=4, padx=5, pady=5)
        self.range_repeat_var = tk.IntVar(value=2)
        range_repeat_spinner = ttk.Spinbox(batch_frame, from_=1, to=10, textvariable=self.range_repeat_var, width=5)
        range_repeat_spinner.grid(row=1, column=5, padx=5, pady=5)
        
        ttk.Button(batch_frame, text="Apply Range", command=self.apply_range).grid(row=1, column=6, padx=5, pady=5)
        
        # Create scroll area
        scroll_frame = ttk.Frame(main_frame)
        scroll_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Create scrollbar
        scrollbar = ttk.Scrollbar(scroll_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create Canvas
        self.canvas = tk.Canvas(scroll_frame)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Configure scrollbar
        scrollbar.config(command=self.canvas.yview)
        self.canvas.config(yscrollcommand=scrollbar.set)
        
        # Create inner frame
        self.inner_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor=tk.NW)
        
        # Create headers
        ttk.Label(self.inner_frame, text="No.", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Label(self.inner_frame, text="Sentence", font=("Arial", 12, "bold")).grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        ttk.Label(self.inner_frame, text="Repeat Count", font=("Arial", 12, "bold")).grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        
        # Create sentence list
        self.repeat_vars = []
        for i, sentence in enumerate(self.sentences):
            # Number
            ttk.Label(self.inner_frame, text=f"{i+1}").grid(row=i+1, column=0, padx=5, pady=5, sticky=tk.W)
            
            # Sentence text
            text_label = ttk.Label(self.inner_frame, text=sentence['text'], wraplength=600)
            text_label.grid(row=i+1, column=1, padx=5, pady=5, sticky=tk.W)
            
            # Repeat count
            repeat_var = tk.IntVar(value=sentence.get('repeat_count', 1))
            self.repeat_vars.append(repeat_var)
            repeat_spinner = ttk.Spinbox(self.inner_frame, from_=0, to=10, textvariable=repeat_var, width=5)
            repeat_spinner.grid(row=i+1, column=2, padx=5, pady=5, sticky=tk.W)
        
        # Update inner frame size
        self.inner_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        
        # Create button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        # Create save button
        save_button = ttk.Button(button_frame, text="Save", command=self.save)
        save_button.pack(side=tk.RIGHT, padx=5)
        
        # Create cancel button
        cancel_button = ttk.Button(button_frame, text="Cancel", command=root.destroy)
        cancel_button.pack(side=tk.RIGHT, padx=5)
        
        # Bind mouse wheel event
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
    
    def apply_batch(self):
        """Apply batch settings"""
        repeat_count = self.batch_repeat_var.get()
        for var in self.repeat_vars:
            var.set(repeat_count)
    
    def apply_range(self):
        """Apply range settings"""
        start = self.range_start_var.get() - 1  # Convert to 0-based index
        end = self.range_end_var.get() - 1  # Convert to 0-based index
        repeat_count = self.range_repeat_var.get()
        
        # Validate range
        if start < 0:
            start = 0
        if end >= len(self.repeat_vars):
            end = len(self.repeat_vars) - 1
        if start > end:
            messagebox.showerror("Error", "Start sentence cannot be greater than end sentence")
            return
        
        # Apply settings
        for i in range(start, end + 1):
            self.repeat_vars[i].set(repeat_count)
    
    def _on_mousewheel(self, event):
        """Mouse wheel event handler"""
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def save(self):
        """Save repeat counts"""
        for i, var in enumerate(self.repeat_vars):
            self.sentences[i]['repeat_count'] = var.get()
        
        # Save subtitle display settings
        subtitle_display = self.subtitle_display_var.get()
        max_chars_per_line = self.max_chars_var.get()
        for sentence in self.sentences:
            sentence['subtitle_display'] = subtitle_display
            sentence['max_chars_per_line'] = max_chars_per_line
        
        self.on_save(self.sentences)
        self.root.destroy()

def format_subtitle_text(text, max_chars_per_line=40):
    """
    Format subtitle text with appropriate line breaks for better readability
    
    Args:
        text: Original subtitle text
        max_chars_per_line: Maximum characters per line
        
    Returns:
        str: Formatted subtitle text with line breaks
    """
    # If text already contains line breaks, we'll respect them but also
    # ensure each line doesn't exceed max_chars_per_line
    if '\n' in text:
        lines = text.split('\n')
        formatted_lines = []
        
        for line in lines:
            # If this line is too long, format it
            if len(line) > max_chars_per_line:
                formatted_lines.extend(format_line(line, max_chars_per_line))
            else:
                formatted_lines.append(line)
        
        return '\n'.join(formatted_lines)
    
    # If text is short enough, return as is
    if len(text) <= max_chars_per_line:
        return text
    
    # Otherwise, format the text
    return '\n'.join(format_line(text, max_chars_per_line))

def format_line(text, max_chars_per_line):
    """
    Format a single line of text into multiple lines
    
    Args:
        text: Text to format
        max_chars_per_line: Maximum characters per line
        
    Returns:
        list: List of formatted lines
    """
    words = text.split()
    lines = []
    current_line = []
    current_length = 0
    
    for word in words:
        # Check if adding this word would exceed the max line length
        word_length = len(word)
        space_length = 1 if current_length > 0 else 0
        
        if current_length + word_length + space_length > max_chars_per_line:
            # If this single word is longer than max_chars_per_line
            if not current_line and word_length > max_chars_per_line:
                # Split the long word
                remaining_word = word
                while len(remaining_word) > 0:
                    chunk = remaining_word[:max_chars_per_line]
                    remaining_word = remaining_word[max_chars_per_line:]
                    lines.append(chunk)
            else:
                # Add the current line to lines and start a new line
                lines.append(' '.join(current_line))
                current_line = [word]
                current_length = word_length
        else:
            # Add word to current line
            current_line.append(word)
            # Add word length plus space
            current_length += word_length + space_length
    
    # Add the last line
    if current_line:
        lines.append(' '.join(current_line))
    
    return lines

def generate_video(video_path, sentences, output_path, progress_callback=None):
    """
    Generate a new video based on sentence information
    
    Args:
        video_path: Path to the original video file
        sentences: List of sentence information
        output_path: Path to the output video file
        progress_callback: Progress callback function
    """
    # Load original video
    video = VideoFileClip(video_path)
    
    # Create clip list
    clips = []
    total_sentences = len(sentences)
    
    # Process each sentence
    for i, sentence in enumerate(sentences):
        # Get sentence start and end time
        start_time = sentence['start']
        end_time = sentence['end']
        repeat_count = sentence.get('repeat_count', 1)
        subtitle_display = sentence.get('subtitle_display', 2)  # Default to show subtitles on the second repeat
        max_chars_per_line = sentence.get('max_chars_per_line', 40)  # Default to 40 characters per line
        
        # Update progress
        if progress_callback:
            progress = (i / total_sentences) * 100
            progress_callback(progress)
        
        # If repeat count is 0, skip this sentence
        if repeat_count <= 0:
            continue
        
        # Ensure time is within video range
        start_time = max(0, start_time)
        end_time = min(video.duration, end_time)
        
        if end_time <= start_time:
            print(f"Warning: Sentence {i+1} has invalid time range, skipping")
            continue
        
        # Extract sentence clip
        sentence_clip = video.subclip(start_time, end_time)
        
        # Create clip with subtitles
        try:
            # Calculate appropriate font size based on video dimensions
            # Smaller videos need smaller font size to prevent overflow
            video_width = sentence_clip.w
            video_height = sentence_clip.h
            
            # Adjust font size based on video width
            # For wider videos, we can use larger font
            if video_width >= 1920:  # Full HD or higher
                fontsize = int(video_height * 0.045)
            elif video_width >= 1280:  # HD
                fontsize = int(video_height * 0.04)
            else:  # SD or smaller
                fontsize = int(video_height * 0.035)
            
            # Adjust max chars per line based on video width
            # This ensures text doesn't overflow horizontally
            adjusted_max_chars = min(max_chars_per_line, int(video_width / 12))
            
            # Format text with line breaks for better readability
            text = format_subtitle_text(sentence['text'], max_chars_per_line=adjusted_max_chars)
            
            # Create text clip with proper styling
            txt_clip = TextClip(
                text, 
                fontsize=fontsize,
                color='white',
                font='Arial',
                stroke_color='white',
                stroke_width=1,  # Increased stroke width for better visibility
                method='label',
                align='center'  # Center-align the text
            ).set_duration(sentence_clip.duration)
            
            # Calculate subtitle position (centered at bottom with safe margin)
            txt_width, txt_height = txt_clip.size
            
            # Ensure subtitle doesn't go off-screen
            # Keep a safe margin from the bottom (8% of video height)
            bottom_margin = int(video_height * 0.08)
            position = ('center', video_height - txt_height - bottom_margin)
            
            # Create a semi-transparent background for better readability
            # Add some padding around the text
            padding_x = int(fontsize * 0.7)  # Horizontal padding
            padding_y = int(fontsize * 0.4)  # Vertical padding
            
            bg_width = txt_width + (padding_x * 2)
            bg_height = txt_height + (padding_y * 2)
            
            # Create a black background with 50% opacity
            bg_clip = ColorClip(
                size=(int(bg_width), int(bg_height)),
                color=(0, 0, 0)
            ).set_opacity(0.5).set_duration(sentence_clip.duration)
            
            # Position the background and text
            bg_position = ('center', video_height - bg_height - bottom_margin + padding_y)
            txt_position = ('center', video_height - txt_height - bottom_margin)
            
            # Composite video, background, and subtitle
            video_with_text = CompositeVideoClip([
                sentence_clip,
                bg_clip.set_position(bg_position),
                txt_clip.set_position(txt_position)
            ])
        except Exception as e:
            print(f"Error adding subtitles: {str(e)}, using clip without subtitles")
            video_with_text = sentence_clip
        
        # Repeat clip specified number of times, showing subtitles according to settings
        for repeat_index in range(repeat_count):
            if subtitle_display == 0:  # 0 means show subtitles on all repeats
                clips.append(video_with_text)
            elif repeat_index == subtitle_display - 1:  # Show subtitles on the specified repeat
                clips.append(video_with_text)
            else:
                clips.append(sentence_clip)  # No subtitles on other repeats
        
        # Print progress
        if subtitle_display == 0:
            subtitle_info = "showing subtitles on all repeats"
        else:
            subtitle_info = f"showing subtitles on repeat {subtitle_display}"
        print(f"Processing sentence {i+1}/{len(sentences)}: repeating {repeat_count} times, {subtitle_info}")
        
        if i <= len(sentences) - 2:
            # Also connect sentences with no speech
            start_time = sentence['end']
            # Start of next sentence
            end_time = sentences[i+1]['start']
            
        sentence_clip = video.subclip(start_time, end_time)
        clips.append(sentence_clip)
    
    # Merge all clips
    if clips:
        # Update progress
        if progress_callback:
            progress_callback(90)  # 90% progress
            
        final_clip = concatenate_videoclips(clips)
        
        # Write video file
        final_clip.write_videofile(
            output_path, 
            codec='libx264', 
            audio_codec='aac'
        )
        
        # Close video
        final_clip.close()
        
        # Update progress
        if progress_callback:
            progress_callback(100)  # 100% progress
    else:
        print("No valid sentence clips")
    
    # Close original video
    video.close()

def load_sentences(json_path):
    """
    Load sentence information from JSON file
    
    Args:
        json_path: Path to JSON file
        
    Returns:
        list: List of sentence information
    """
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_sentences(sentences, json_path):
    """
    Save sentence information to JSON file
    
    Args:
        sentences: List of sentence information
        json_path: Path to JSON file
    """
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(sentences, f, ensure_ascii=False, indent=2)

def main_gui():
    """GUI main function"""
    root = tk.Tk()
    root.title("Shadow Reading Video Generator")
    root.geometry("600x400")
    
    # Create main frame
    main_frame = ttk.Frame(root, padding=20)
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # Video file selection
    ttk.Label(main_frame, text="Video file:").grid(row=0, column=0, sticky=tk.W, pady=5)
    video_path_var = tk.StringVar()
    ttk.Entry(main_frame, textvariable=video_path_var, width=50).grid(row=0, column=1, pady=5)
    ttk.Button(main_frame, text="Browse...", command=lambda: video_path_var.set(filedialog.askopenfilename(
        title="Select video file",
        filetypes=[("Video files", "*.mp4 *.avi *.mkv *.mov"), ("All files", "*.*")]
    ))).grid(row=0, column=2, padx=5, pady=5)
    
    # JSON file selection
    ttk.Label(main_frame, text="JSON file:").grid(row=1, column=0, sticky=tk.W, pady=5)
    json_path_var = tk.StringVar()
    ttk.Entry(main_frame, textvariable=json_path_var, width=50).grid(row=1, column=1, pady=5)
    ttk.Button(main_frame, text="Browse...", command=lambda: json_path_var.set(filedialog.askopenfilename(
        title="Select JSON file",
        filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
    ))).grid(row=1, column=2, padx=5, pady=5)
    
    # Output file selection
    ttk.Label(main_frame, text="Output file:").grid(row=2, column=0, sticky=tk.W, pady=5)
    output_path_var = tk.StringVar(value="output.mp4")
    ttk.Entry(main_frame, textvariable=output_path_var, width=50).grid(row=2, column=1, pady=5)
    ttk.Button(main_frame, text="Browse...", command=lambda: output_path_var.set(filedialog.asksaveasfilename(
        title="Save output file",
        defaultextension=".mp4",
        filetypes=[("MP4 files", "*.mp4"), ("All files", "*.*")]
    ))).grid(row=2, column=2, padx=5, pady=5)
    
    # Create button frame
    button_frame = ttk.Frame(main_frame)
    button_frame.grid(row=3, column=0, columnspan=3, pady=20)
    
    def edit_sentences():
        """Edit sentence repeat counts"""
        video_path = video_path_var.get()
        json_path = json_path_var.get()
        
        if not json_path:
            messagebox.showerror("Error", "Please select a JSON file")
            return
        
        try:
            sentences = load_sentences(json_path)
            
            # Create new window
            editor_root = tk.Toplevel(root)
            
            def on_save(updated_sentences):
                """Save updated sentence information"""
                save_sentences(updated_sentences, json_path)
                messagebox.showinfo("Success", f"Sentence repeat counts saved to: {json_path}")
            
            # Create sentence editor
            editor = SentenceEditor(editor_root, sentences, on_save)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error loading sentence information: {str(e)}")
    
    def generate():
        """Generate video"""
        video_path = video_path_var.get()
        json_path = json_path_var.get()
        output_path = output_path_var.get()
        
        if not video_path:
            messagebox.showerror("Error", "Please select a video file")
            return
        
        if not json_path:
            messagebox.showerror("Error", "Please select a JSON file")
            return
        
        if not output_path:
            messagebox.showerror("Error", "Please specify an output file")
            return
        
        try:
            sentences = load_sentences(json_path)
            
            # Disable buttons
            for widget in button_frame.winfo_children():
                widget.configure(state="disabled")
            
            # Show progress window
            progress_window = tk.Toplevel(root)
            progress_window.title("Processing")
            progress_window.geometry("300x100")
            
            ttk.Label(progress_window, text="Generating video, please wait...").pack(pady=10)
            
            progress_var = tk.DoubleVar()
            progress_bar = ttk.Progressbar(progress_window, variable=progress_var, maximum=100)
            progress_bar.pack(fill=tk.X, padx=20, pady=10)
            
            # Progress callback function
            def update_progress(progress):
                progress_var.set(progress)
                progress_window.update_idletasks()
            
            # Generate video in a new thread
            import threading
            
            def process_video():
                try:
                    generate_video(video_path, sentences, output_path, update_progress)
                    
                    # Update UI
                    root.after(0, lambda: [
                        progress_window.destroy(),
                        messagebox.showinfo("Success", f"Video generation complete: {output_path}"),
                        # Enable buttons
                        [widget.configure(state="normal") for widget in button_frame.winfo_children()]
                    ])
                    
                except Exception as e:
                    # Update UI
                    root.after(0, lambda: [
                        progress_window.destroy(),
                        messagebox.showerror("Error", f"Error generating video: {str(e)}"),
                        # Enable buttons
                        [widget.configure(state="normal") for widget in button_frame.winfo_children()]
                    ])
            
            thread = threading.Thread(target=process_video)
            thread.daemon = True
            thread.start()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error processing video: {str(e)}")
    
    # Edit sentences button
    ttk.Button(button_frame, text="Edit Sentence Repeat Counts", command=edit_sentences).pack(side=tk.LEFT, padx=5)
    
    # Generate video button
    ttk.Button(button_frame, text="Generate Video", command=generate).pack(side=tk.LEFT, padx=5)
    
    # Exit button
    ttk.Button(button_frame, text="Exit", command=root.quit).pack(side=tk.LEFT, padx=5)
    
    # Set column weights
    main_frame.columnconfigure(1, weight=1)
    
    # Run main loop
    root.mainloop()

def main_cli():
    """Command line main function"""
    parser = argparse.ArgumentParser(description='Generate shadow reading video based on sentence information')
    parser.add_argument('--video', required=True, help='Path to original video file')
    parser.add_argument('--json', required=True, help='Path to sentence information JSON file')
    parser.add_argument('--output', default='output.mp4', help='Path to output video file')
    parser.add_argument('--edit', action='store_true', help='Edit sentence repeat counts')
    parser.add_argument('--subtitle-display', type=int, default=2, 
                        help='Show subtitles on which repeat (0=All repeats, 1=First repeat, 2=Second repeat, ...)')
    parser.add_argument('--max-chars-per-line', type=int, default=40,
                        help='Maximum characters per line for subtitles (default: 40)')
    
    args = parser.parse_args()
    
    try:
        # Load sentence information
        sentences = load_sentences(args.json)
        
        # If editing sentence repeat counts
        if args.edit:
            root = tk.Tk()
            root.title("Sentence Repeat Count Editor")
            
            def on_save(updated_sentences):
                save_sentences(updated_sentences, args.json)
                print(f"Sentence repeat counts saved to: {args.json}")
                root.quit()
            
            editor = SentenceEditor(root, sentences, on_save)
            root.mainloop()
            
            # Reload updated sentence information
            sentences = load_sentences(args.json)
        else:
            # If not editing, apply subtitle display setting from command line
            for sentence in sentences:
                sentence['subtitle_display'] = args.subtitle_display
                sentence['max_chars_per_line'] = args.max_chars_per_line
            
            # Save updated settings
            save_sentences(sentences, args.json)
        
        # Generate video
        generate_video(args.video, sentences, args.output)
        
        print(f"Video generation complete: {args.output}")
        
    except Exception as e:
        print(f"Error processing video: {str(e)}")

if __name__ == "__main__":
    # Check if there are command line arguments
    if len(os.sys.argv) > 1:
        main_cli()
    else:
        main_gui()
