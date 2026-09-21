"""Integrity checker — verifies pins survive compression."""

import re
from dataclasses import dataclass, field
from typing import List

from lane_a_context_engine.pin_extraction import PinCandidate, PinType


@dataclass
class IntegrityViolation:
    """A single pin integrity violation."""
    pin_id: str
    issue: str
    severity: str = "warning"  # warning, error


@dataclass
class IntegrityReport:
    """Report from a pin integrity check."""
    compression_event_id: str
    checked_pins: int = 0
    preserved_correctly: int = 0
    weakened: int = 0
    lost: int = 0
    violations: List[IntegrityViolation] = field(default_factory=list)


class IntegrityChecker:
    """Checks whether pinned information survived compression."""

    def check(self, pins: List[PinCandidate], summary: str, compression_event_id: str = "") -> IntegrityReport:
        """Check if pins survived in the summary."""
        report = IntegrityReport(compression_event_id=compression_event_id)
        report.checked_pins = len(pins)

        for pin in pins:
            if pin.pin_type == PinType.PRESERVE_EXACT:
                # Exact pins should have their key phrases in the summary
                if not self._check_exact(pin.content, summary):
                    if self._check_partial(pin.content, summary):
                        report.weakened += 1
                        report.violations.append(IntegrityViolation(
                            pin_id=pin.pin_id,
                            issue=f"Preserve exact pin was paraphrased: '{pin.content[:60]}...'",
                            severity="warning",
                        ))
                    else:
                        report.lost += 1
                        report.violations.append(IntegrityViolation(
                            pin_id=pin.pin_id,
                            issue=f"Preserve exact pin was lost: '{pin.content[:60]}...'",
                            severity="error",
                        ))
                else:
                    report.preserved_correctly += 1

            elif pin.pin_type == PinType.PRESERVE_MEANING:
                # Meaning pins can be rephrased but key concepts should appear
                if not self._check_meaning(pin.content, summary):
                    report.weakened += 1
                    report.violations.append(IntegrityViolation(
                        pin_id=pin.pin_id,
                        issue=f"Preserve meaning pin may have lost meaning: '{pin.content[:60]}...'",
                        severity="warning",
                    ))
                else:
                    report.preserved_correctly += 1

            elif pin.pin_type == PinType.PRESERVE_RELATIONSHIP:
                # Relationship pins should have both entities mentioned
                if not self._check_relationship(pin.content, summary):
                    report.weakened += 1
                    report.violations.append(IntegrityViolation(
                        pin_id=pin.pin_id,
                        issue=f"Relationship pin weakened: '{pin.content[:60]}...'",
                        severity="warning",
                    ))
                else:
                    report.preserved_correctly += 1

            else:
                # Other types: just check if content is roughly present
                if self._check_partial(pin.content, summary):
                    report.preserved_correctly += 1
                else:
                    report.lost += 1
                    report.violations.append(IntegrityViolation(
                        pin_id=pin.pin_id,
                        issue=f"Pin not found in summary: '{pin.content[:60]}...'",
                        severity="error",
                    ))

        return report

    def _check_exact(self, original: str, summary: str) -> bool:
        """Check if exact wording is preserved (at least key phrases)."""
        # Extract key phrases (quoted text, technical terms, short phrases)
        key_phrases = re.findall(r'"([^"]+)"', original)
        key_phrases += re.findall(r"'([^']+)'", original)
        if not key_phrases:
            # Use first 30 chars as key phrase
            key_phrases = [original[:30].strip()]

        for phrase in key_phrases:
            if phrase.lower() in summary.lower():
                return True
        return False

    def _check_partial(self, original: str, summary: str) -> bool:
        """Check if at least some of the original content appears (using meaningful words)."""
        stopwords = {"the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
                     "have", "has", "had", "do", "does", "did", "will", "would", "could",
                     "should", "may", "might", "can", "shall", "to", "of", "in", "for",
                     "on", "with", "at", "by", "from", "as", "into", "through", "during",
                     "before", "after", "above", "below", "between", "out", "off", "over",
                     "under", "again", "further", "then", "once", "and", "but", "or", "nor",
                     "not", "so", "than", "too", "very", "just", "about", "this", "that",
                     "these", "those", "it", "its", "i", "we", "you", "they", "he", "she",
                     "my", "your", "his", "her", "our", "their", "what", "which", "who",
                     "when", "where", "why", "how", "all", "each", "every", "both", "few",
                     "more", "most", "other", "some", "such", "no", "only", "own", "same",
                     "there", "here", "up", "down", "if", "because", "while", "although",
                     "until", "since", "however", "therefore", "thus", "hence"}
        words = [w.lower() for w in re.findall(r'\b[a-z]{3,}\b', original) if w.lower() not in stopwords]
        if not words:
            return original.lower() in summary.lower()
        matches = sum(1 for w in words if w in summary.lower())
        return matches / len(words) >= 0.4

    def _check_meaning(self, original: str, summary: str) -> bool:
        """Check if meaning is preserved (keywords appear)."""
        # Extract meaningful words (nouns, verbs — skip stopwords)
        stopwords = {"the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
                     "have", "has", "had", "do", "does", "did", "will", "would", "could",
                     "should", "may", "might", "can", "shall", "to", "of", "in", "for",
                     "on", "with", "at", "by", "from", "as", "into", "through", "during",
                     "before", "after", "above", "below", "between", "out", "off", "over",
                     "under", "again", "further", "then", "once", "and", "but", "or", "nor",
                     "not", "so", "than", "too", "very", "just", "about", "this", "that",
                     "these", "those", "it", "its", "i", "we", "you", "they", "he", "she",
                     "my", "your", "his", "her", "our", "their", "what", "which", "who",
                     "when", "where", "why", "how", "all", "each", "every", "both", "few",
                     "more", "most", "other", "some", "such", "no", "only", "own", "same",
                     "there", "here", "up", "down", "if", "because", "while", "although",
                     "until", "since", "although", "however", "therefore", "thus", "hence"}
        words = [w.lower() for w in re.findall(r'\b[a-z]{3,}\b', original) if w.lower() not in stopwords]
        if not words:
            return True
        matches = sum(1 for w in words if w in summary.lower())
        return matches / len(words) >= 0.4

    def _check_relationship(self, original: str, summary: str) -> bool:
        """Check if relationship is preserved (both entities AND connection)."""
        # Extract relationship keywords
        relationship_keywords = ["feeds into", "connected to", "depends on", "relates to",
                                 "connected with", "linked to", "feeds from", "flows into",
                                 "flows from", "provides to", "sends to"]
        original_lower = original.lower()
        summary_lower = summary.lower()
        
        # Check if any relationship keyword from original appears in summary
        for kw in relationship_keywords:
            if kw in original_lower and kw not in summary_lower:
                return False  # Relationship keyword missing
        
        # Also check that at least 2 entities appear
        entities = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', original)
        if len(entities) < 2:
            entities = re.findall(r'\b(?:the |a |an )?([a-z]+(?:\s+[a-z]+)?\b)', original_lower)
            entities = [e for e in entities if len(e) > 3]
        if len(entities) < 2:
            return self._check_partial(original, summary)
        matches = sum(1 for e in entities if e.lower() in summary_lower)
        return matches >= 2
