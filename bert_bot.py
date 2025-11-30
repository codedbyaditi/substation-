from .knowledge_base import EQUIPMENT_DATA
import random

class SubstationChatbot:
    def __init__(self):
        self.data = EQUIPMENT_DATA

    def find_equipment(self, query):
        query = query.lower()
        matches = []
        for item in self.data:
            name = item['equipment']
            name_lower = name.lower()
            # Base name without parenthetical suffix, e.g., "Circuit Breaker (SF6 / Vacuum)" -> "circuit breaker"
            base_name_lower = name_lower.split('(')[0].strip()
            # Direct substring match on full name
            if name_lower in query:
                matches.append(item)
                continue
            # Match if query contains base name (more forgiving)
            if base_name_lower and base_name_lower in query:
                matches.append(item)
                continue

            # Match acronym inside parentheses, e.g., "Gas Insulated Switchgear (GIS)" -> gis
            acronym = None
            if '(' in name and ')' in name:
                try:
                    acronym = name[name.index('(')+1:name.index(')')].lower()
                except Exception:
                    acronym = None
            if acronym and acronym in query:
                matches.append(item)
                continue

            # Simple alias heuristics for common equipment
            aliases = {
                'gis': 'gas insulated switchgear',
                'cb': 'circuit breaker',
                'ct': 'current transformer',
                'pt': 'potential transformer',
                'avr': 'automatic voltage regulator',
                'opgw': 'optical ground wire'
            }
            for alias, canonical in aliases.items():
                if alias in query and canonical in name_lower:
                    matches.append(item)
                    break
        return matches

    def get_response(self, query):
        query = query.lower()
        
        # Check for specific equipment
        matches = self.find_equipment(query)
        
        if matches:
            equipment = matches[0]
            name = equipment['equipment']
            
            if "tool" in query:
                return (f"For **{name}**, you should use: {', '.join(equipment['tools'])}.", random.randint(80, 95))
            elif "prevent" in query or "maintain" in query or "maintenance" in query:
                return (f"**Preventive Maintenance for {name}:**\n" + "\n".join([f"- {task}" for task in equipment['preventive_maintenance']]), random.randint(75, 90))
            elif "fail" in query or "symptom" in query or "problem" in query:
                return (f"**Common Failure Symptoms for {name}:**\n" + "\n".join([f"- {symptom}" for symptom in equipment['failure_symptoms']]), random.randint(70, 88))
            elif "safe" in query or "precaution" in query:
                return (f"**Safety Precautions for {name}:**\n" + "\n".join([f"- {precaution}" for precaution in equipment['safety_precautions']]), random.randint(80, 95))
            else:
                return (f"I found information about **{name}**. You can ask me about its tools, maintenance, failure symptoms, or safety precautions.", random.randint(60, 80))

        # General conversational fallbacks
        if "hello" in query or "hi" in query:
            return (
                "Hello! I answer substation maintenance queries based on the knowledge base (equipment, tools, preventive tasks, failures, safety). Please mention the equipment, e.g., 'Safety for GIS' or 'Maintenance for Power Transformer'.",
                random.randint(50, 70)
            )
        elif "help" in query:
            return ("I can help you with maintenance procedures, tools, and safety for substation equipment. Try asking 'How to maintain Power Transformer?' or 'Tools for Circuit Breaker'.", random.randint(55, 75))
        
        return ("I'm not sure about that specific equipment. Please specify the equipment name (e.g., 'Power Transformer', 'Circuit Breaker').", 0)
