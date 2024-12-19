from pathlib import Path
import json

CorrectL = [{"Original": "Chris Sloan", "Updated": "Christopher Sloan"},
            {"Original": "chris sloan", "Updated": "Christopher Sloan"},
            {"Original": "James High Sr", "Updated": "James High Sr."},
            {"Original": "james high sr", "Updated": "James High Sr."},
            {"Original": "james high", "Updated": "James High Sr."},
            {"Original": "James High", "Updated": "James High Sr."}, 
            {"Original": "James high", "Updated": "James High Sr."}, 
            {"Original": "james High", "Updated": "James High Sr."}, 
            {"Original": "Jim High Sr", "Updated": "James High Sr."},
            {"Original": "james A High", "Updated": "James High Sr."},         
            {"Original": "J.High Sr", "Updated": "James High Sr."},
            {"Original": "toni high", "Updated": "Toni High"},
            {"Original": "john taylor", "Updated": "John Taylor"},
            {"Original": "carla maras", "Updated": "Carla Marras"},
            {"Original": "Carla Maras", "Updated": "Carla Marras"},
            {"Original": "Brian Durobrow", "Updated": "Brian Durborow"},
            {"Original": "Brian Duborow", "Updated": "Brian Durborow"},
            {"Original": "brian duborow", "Updated": "Brian Durborow"},
            {"Original": "brian dubborow", "Updated": "Brian Durborow"},
            {"Original": "Brian Dubowrow", "Updated": "Brian Durborow"},
            {"Original": "Brian Dubrow", "Updated": "Brian Durborow"},
            {"Original": "conlon keenan", "Updated": "Conlyn Keenan"},
            {"Original": "Joey Klien", "Updated": "Joseph Klein"},
            {"Original": "Joey Kline", "Updated": "Joseph Klein"},
            {"Original": "joey kline", "Updated": "Joseph Klein"},
            {"Original": "linda picirillo", "Updated": "Linda Picirillo"},
            {"Original": "Jeff   Sutherlin", "Updated": "Jeff Sutherlin"},
            {"Original": "cassidy mueller", "Updated": "Cassidy Muller"}]

path = Path('WEFAS_corrections.json')
contents = json.dumps(CorrectL)
path.write_text(contents)
