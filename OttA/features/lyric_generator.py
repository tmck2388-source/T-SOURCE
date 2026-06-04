"""
Lyric Generator
Generate creative music lyrics with explicit content, custom BPM, and beat syncing
"""
from typing import Optional, Dict, List
import json
import math

class LyricGenerator:
    """Generate music lyrics with custom specifications"""
    
    def __init__(self, ai_client):
        self.ai_client = ai_client
        self.templates = self.load_templates()
        self.generated_lyrics = []
    
    def load_templates(self) -> Dict:
        """Load lyric templates"""
        return {
            "rap": {
                "style": "rap",
                "rhyme_scheme": "AABB",
                "tempo": 90,
                "bars": 16
            },
            "hip_hop": {
                "style": "hip_hop",
                "rhyme_scheme": "ABAB",
                "tempo": 85,
                "bars": 8
            },
            "drill": {
                "style": "drill",
                "rhyme_scheme": "AABBB",
                "tempo": 140,
                "bars": 16
            },
            "trap": {
                "style": "trap",
                "rhyme_scheme": "AABB",
                "tempo": 140,
                "bars": 12
            }
        }
    
    def generate_lyrics(
        self,
        story: Optional[str] = None,
        keywords: Optional[List[str]] = None,
        bpm: int = 90,
        style: str = "rap",
        bars: int = 16,
        explicit: bool = True
    ) -> str:
        """
        Generate lyrics based on user input
        
        Args:
            story: Optional story/narrative to build lyrics around
            keywords: Optional keywords to incorporate
            bpm: Beats per minute (affects syllable density)
            style: Musical style (rap, hip_hop, drill, trap)
            bars: Number of bars to generate
            explicit: Allow explicit content
        
        Returns:
            Generated lyrics
        """
        
        prompt = f"""Generate {bars} bars of {style} lyrics with the following specifications:
- BPM: {bpm}
- Explicit content: {'Yes, include explicit language and adult themes' if explicit else 'No explicit content'}
- Style: {style}
"""
        
        if story:
            prompt += f"- Story/Theme: {story}\n"
        
        if keywords:
            prompt += f"- Keywords to include: {', '.join(keywords)}\n"
        
        prompt += """\nFormat the output as:
[Verse 1]
{lyrics lines here}

[Hook]
{catchy chorus}

Requirements:
- Each line should sync with the beat (syllable count relevant to BPM)
- Maintain consistent rhyme scheme
- Natural flow and rhythm
- Original content
"""
        
        response = self.ai_client.generate(prompt)
        
        self.generated_lyrics.append({
            "style": style,
            "bpm": bpm,
            "bars": bars,
            "lyrics": response,
            "input_story": story,
            "keywords": keywords
        })
        
        return response
    
    def sync_to_song(
        self,
        lyrics: str,
        target_bpm: int,
        original_bpm: int = 90
    ) -> str:
        """
        Adjust lyrics to sync with a specific BPM/song
        
        Args:
            lyrics: The lyrics to adjust
            target_bpm: Target BPM of the song
            original_bpm: Original BPM the lyrics were generated for
        
        Returns:
            Adjusted lyrics
        """
        
        ratio = target_bpm / original_bpm
        
        prompt = f"""Adjust the following lyrics to fit a song with {target_bpm} BPM.
Original BPM was {original_bpm}. Adjust syllable counts and flow accordingly (ratio: {ratio:.2f}).

Original lyrics:
{lyrics}

Rewrite to:
- Maintain meaning and story
- Fit the new tempo
- Keep rhyme schemes and flow smooth
- Adjust syllable density to {target_bpm} BPM
"""
        
        return self.ai_client.generate(prompt)
    
    def add_beat_markers(self, lyrics: str, bpm: int) -> str:
        """Add beat/timing markers to lyrics"""
        lines = lyrics.split('\n')
        marked_lyrics = []
        
        for i, line in enumerate(lines):
            if line.strip():
                # Calculate beat position
                beat_pos = (i % 4) + 1
                marked_lyrics.append(f"[{beat_pos}] {line}")
            else:
                marked_lyrics.append(line)
        
        return '\n'.join(marked_lyrics)
    
    def get_history(self) -> List[Dict]:
        """Get generated lyrics history"""
        return self.generated_lyrics

# Example usage function
def demo_lyric_generation(ai_client):
    generator = LyricGenerator(ai_client)
    
    lyrics = generator.generate_lyrics(
        story="Street life and overcoming struggles",
        keywords=["hustle", "grind", "success"],
        bpm=90,
        style="rap",
        bars=8,
        explicit=True
    )
    
    print("Generated Lyrics:")
    print(lyrics)
    
    return lyrics