#Here is the Python file `activity_generate_marketing_content.py` that meets the specified requirements:

import logging
from typing import Dict, Any, List
from framework.activity_decorator import activity, ActivityBase, ActivityResult
from activities.activity_draw import DrawActivity
from skills.skill_generate_image import ImageGenerationSkill
from framework.memory import Memory

logger = logging.getLogger(__name__)

@activity(
    name="Generate Visually Compelling Marketing Content",
    energy_cost=1.0,
    cooldown=3600,
    required_skills=["image_generation"]
)
class GenerateMarketingContentActivity(DrawActivity):
    """Creates eye-catching images, infographics, and visuals to enhance marketing materials and social media posts."""
       
    def _get_recent_memories(self, shared_data, limit: int = 1) -> List[str]:
        """
        Fetch the last N memories (activity_type='GenerateMarketingContentActivity') from memory.
        """
        system_data = shared_data.get_category_data("system")
        memory_obj: Memory = system_data.get("memory_ref")

        if not memory_obj:
            from framework.main import DigitalBeing

            being = DigitalBeing()
            being.initialize()
            memory_obj = being.memory

        recent_activities = memory_obj.get_recent_activities(limit=50, offset=0)
        images = []
        for act in recent_activities:
            if act.get("activity_type") == "GenerateMarketingContentActivity" and act.get("success"):
                image_body = act.get("data", {}).get("prompt", "")
                if image_body:
                    images.append(image_body)

        return images[:limit]

    def _generate_prompt(self, shared_data) -> str:
        """Generate a drawing prompt based on current state and memory."""
        state = shared_data.get("state", "current_state", {})
        
        past_images = self._get_recent_memories(shared_data)

        personality = state.get("personality", {})
        mood = state.get("mood", "neutral")

        # Base prompts for different moods
        mood_prompts = {
            "happy": "innovative and eye-catching visuals",
            "neutral": "promotional flyer or poster with bold text and vibrant colors",
            "sad": "a photo-like image",
        }

        # Get base prompt from mood
        base_prompt = mood_prompts.get(mood, mood_prompts["neutral"])

        # Modify based on personality
        if personality.get("creativity", 0) > 0.7:
            base_prompt += " with surreal elements"
        if personality.get("curiosity", 0) > 0.7:
            base_prompt += " featuring unexpected details"

        return f"Digital artwork of {base_prompt}, digital art style, different from the prior prompt: {past_images}"
