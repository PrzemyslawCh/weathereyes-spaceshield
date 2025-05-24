"""
WeatherEyes - Event Images Upload
Interfejs do dodawania prawdziwych zdjęć z wydarzenia
"""

import os
import shutil
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk

# Dodaj ścieżki
import sys
sys.path.append(str(Path(__file__).parent))

from ai_model.openai_vision import OpenAIVisionAnalyzer
from bot.real_alerts import RealAlertSystem

class EventImageUploader:
    def __init__(self):
        self.event_images_dir = Path("data/event_images")
        self.event_images_dir.mkdir(parents=True, exist_ok=True)
        
        self.uploaded_images = []
        self.analyses = []
        
        # Initialize AI components
        self.vision_analyzer = OpenAIVisionAnalyzer()
        self.alert_system = RealAlertSystem()
        
        # Setup GUI
        self.setup_gui()
    
    def setup_gui(self):
        """Tworzy interfejs graficzny"""
        
        self.root = tk.Tk()
        self.root.title("WeatherEyes - Upload Zdjęć z Wydarzenia")
        self.root.geometry("800x600")
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="🌤️ WeatherEyes - Upload Zdjęć z Wydarzenia", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=10)
        
        # Instructions
        instructions = ttk.Label(main_frame, 
                                text="Dodaj swoje screenshoty z wydarzenia SHAMAN 2024\nAI przeanalizuje warunki pogodowe i wyśle prawdziwe alerty!",
                                font=("Arial", 10))
        instructions.grid(row=1, column=0, columnspan=3, pady=5)
        
        # Upload button
        upload_btn = ttk.Button(main_frame, text="📁 Wybierz Zdjęcia", command=self.upload_images)
        upload_btn.grid(row=2, column=0, pady=10, padx=5)
        
        # Analyze button
        analyze_btn = ttk.Button(main_frame, text="🔍 Analizuj AI", command=self.analyze_images)
        analyze_btn.grid(row=2, column=1, pady=10, padx=5)
        
        # Send alerts button
        alerts_btn = ttk.Button(main_frame, text="🚨 Wyślij Alerty", command=self.send_alerts)
        alerts_btn.grid(row=2, column=2, pady=10, padx=5)
        
        # Images list
        list_frame = ttk.LabelFrame(main_frame, text="Zdjęcia", padding="5")
        list_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        # Images listbox with scrollbar
        listbox_frame = ttk.Frame(list_frame)
        listbox_frame.pack(fill=tk.BOTH, expand=True)
        
        self.images_listbox = tk.Listbox(listbox_frame, height=8)
        scrollbar = ttk.Scrollbar(listbox_frame, orient=tk.VERTICAL, command=self.images_listbox.yview)
        self.images_listbox.configure(yscrollcommand=scrollbar.set)
        
        self.images_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Results area
        results_frame = ttk.LabelFrame(main_frame, text="Wyniki Analizy", padding="5")
        results_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        self.results_text = tk.Text(results_frame, height=8, wrap=tk.WORD)
        results_scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.results_text.yview)
        self.results_text.configure(yscrollcommand=results_scrollbar.set)
        
        self.results_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        results_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Gotowy do uploadu zdjęć...")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var)
        status_bar.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.columnconfigure(2, weight=1)
        main_frame.rowconfigure(3, weight=1)
        main_frame.rowconfigure(4, weight=1)
    
    def upload_images(self):
        """Upload zdjęć z wydarzenia"""
        
        file_types = [
            ("Image files", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff"),
            ("JPEG files", "*.jpg *.jpeg"),
            ("PNG files", "*.png"),
            ("All files", "*.*")
        ]
        
        filenames = filedialog.askopenfilenames(
            title="Wybierz zdjęcia z wydarzenia",
            filetypes=file_types
        )
        
        if not filenames:
            return
        
        self.status_var.set(f"Kopiuję {len(filenames)} zdjęć...")
        self.root.update()
        
        # Copy images to event folder
        copied_count = 0
        for filename in filenames:
            try:
                source_path = Path(filename)
                
                # Generate unique filename
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                new_filename = f"event_{timestamp}_{copied_count:03d}{source_path.suffix}"
                destination = self.event_images_dir / new_filename
                
                # Copy file
                shutil.copy2(source_path, destination)
                self.uploaded_images.append(str(destination))
                
                # Add to listbox
                display_name = f"{new_filename} ({source_path.name})"
                self.images_listbox.insert(tk.END, display_name)
                
                copied_count += 1
                
            except Exception as e:
                messagebox.showerror("Błąd", f"Nie można skopiować {filename}: {e}")
        
        self.status_var.set(f"Skopiowano {copied_count} zdjęć. Gotowy do analizy AI.")
        
        if copied_count > 0:
            messagebox.showinfo("Sukces", f"Skopiowano {copied_count} zdjęć z wydarzenia!")
    
    def analyze_images(self):
        """Analizuje zdjęcia używając OpenAI Vision"""
        
        if not self.uploaded_images:
            messagebox.showwarning("Brak zdjęć", "Najpierw dodaj zdjęcia z wydarzenia!")
            return
        
        self.status_var.set("Analizuję zdjęcia z OpenAI Vision API...")
        self.root.update()
        
        # Clear previous results
        self.results_text.delete(1.0, tk.END)
        self.analyses = []
        
        context = "Zdjęcia z wydarzenia SHAMAN 2024 - hackathon technologiczny"
        
        try:
            # Analyze images
            self.analyses = self.vision_analyzer.batch_analyze_images(
                self.uploaded_images, context
            )
            
            # Display results
            self.display_analysis_results()
            
            self.status_var.set(f"Przeanalizowano {len(self.analyses)} zdjęć. Gotowy do wysyłania alertów.")
            
            # Show summary
            summary = self.vision_analyzer.get_weather_summary_from_images(self.analyses)
            
            if 'error' not in summary:
                messagebox.showinfo(
                    "Analiza Zakończona",
                    f"Dominująca pogoda: {summary['dominant_weather']}\n"
                    f"Średnia pewność: {summary['confidence']:.1%}\n"
                    f"Przeanalizowano: {summary['valid_analyses']}/{summary['total_images_analyzed']} zdjęć"
                )
            
        except Exception as e:
            messagebox.showerror("Błąd analizy", f"Wystąpił błąd podczas analizy: {e}")
            self.status_var.set("Błąd analizy!")
    
    def display_analysis_results(self):
        """Wyświetla wyniki analizy"""
        
        self.results_text.delete(1.0, tk.END)
        
        for i, analysis in enumerate(self.analyses, 1):
            image_name = Path(analysis.get('image_path', '')).name
            weather = analysis.get('weather_condition', 'unknown')
            confidence = analysis.get('confidence', 0)
            description = analysis.get('description', 'Brak opisu')
            
            result_text = f"[{i}] {image_name}\n"
            result_text += f"    🌤️ Pogoda: {weather} ({confidence:.1%} pewności)\n"
            result_text += f"    📝 Opis: {description}\n"
            
            if analysis.get('reasoning'):
                result_text += f"    🤔 Uzasadnienie: {analysis['reasoning']}\n"
            
            result_text += "\n" + "="*50 + "\n\n"
            
            self.results_text.insert(tk.END, result_text)
        
        # Add summary
        if self.analyses:
            summary = self.vision_analyzer.get_weather_summary_from_images(self.analyses)
            
            if 'error' not in summary:
                summary_text = "\n📊 PODSUMOWANIE:\n"
                summary_text += f"Dominująca pogoda: {summary['dominant_weather']}\n"
                summary_text += f"Średnia pewność: {summary['confidence']:.1%}\n"
                summary_text += f"Przeanalizowane zdjęcia: {summary['valid_analyses']}/{summary['total_images_analyzed']}\n\n"
                
                summary_text += "Rozkład pogody:\n"
                for weather, info in summary.get('weather_distribution', {}).items():
                    avg_conf = info['total_confidence'] / info['count']
                    summary_text += f"  • {weather}: {info['count']} zdjęć ({avg_conf:.1%} śr. pewność)\n"
                
                self.results_text.insert(tk.END, summary_text)
    
    def send_alerts(self):
        """Wysyła prawdziwe alerty na podstawie analizy"""
        
        if not self.analyses:
            messagebox.showwarning("Brak analizy", "Najpierw przeanalizuj zdjęcia!")
            return
        
        self.status_var.set("Wysyłam alerty przez Telegram i SMS...")
        self.root.update()
        
        try:
            # Send individual image analysis alerts
            sent_alerts = 0
            for analysis in self.analyses:
                if analysis.get('weather_condition') != 'unknown':
                    alert_result = self.alert_system.send_image_analysis_alert(
                        analysis['image_path'], analysis
                    )
                    
                    if alert_result['results']['telegram']['success']:
                        sent_alerts += 1
            
            # Send summary alert
            summary = self.vision_analyzer.get_weather_summary_from_images(self.analyses)
            if 'error' not in summary:
                summary_alert = self.alert_system.send_daily_summary_alert(summary, "SHAMAN 2024 Event")
                if summary_alert['results']['telegram']['success']:
                    sent_alerts += 1
            
            # Show results
            stats = self.alert_system.get_alert_stats()
            
            self.status_var.set(f"Wysłano {sent_alerts} alertów!")
            
            messagebox.showinfo(
                "Alerty Wysłane!",
                f"Wysłano {sent_alerts} alertów\n\n"
                f"Telegram: {stats['successful_telegram']}/{stats['total_alerts']} sukces\n"
                f"SMS: {stats['successful_sms']}/{stats['total_alerts']} sukces\n\n"
                f"Sprawdź swój telefon/Telegram!"
            )
            
        except Exception as e:
            messagebox.showerror("Błąd alertów", f"Wystąpił błąd podczas wysyłania: {e}")
            self.status_var.set("Błąd wysyłania alertów!")
    
    def run(self):
        """Uruchamia aplikację"""
        print("🚀 Uruchamiam WeatherEyes Event Images Uploader...")
        print("📱 Dodaj zdjęcia z wydarzenia i zobacz prawdziwe alerty AI!")
        self.root.mainloop()

def main():
    """Main function"""
    
    print("🌤️ WeatherEyes - Event Images Upload System")
    print("=" * 50)
    print("📸 Dodaj swoje screenshoty z wydarzenia SHAMAN 2024")
    print("🤖 AI przeanalizuje pogodę i wyśle prawdziwe alerty")
    print("📱 Alerty będą wysłane przez Telegram i SMS")
    print("=" * 50)
    
    # Check for required directories
    Path("data/event_images").mkdir(parents=True, exist_ok=True)
    
    # Start GUI
    app = EventImageUploader()
    app.run()

if __name__ == "__main__":
    main() 