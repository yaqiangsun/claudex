"""Lorem Ipsum Skill - Python implementation of src/skills/bundled/loremIpsum.ts"""
from __future__ import annotations
import random
from typing import Any

from pyclaude.skills.bundled import BundledSkillDefinition, register_bundled_skill, is_ant_user


# One-token words for lorem ipsum (verified via API token counting)
ONE_TOKEN_WORDS = [
    # Articles & pronouns
    'the', 'a', 'an', 'I', 'you', 'he', 'she', 'it', 'we', 'they',
    'me', 'him', 'her', 'us', 'them', 'my', 'your', 'his', 'its', 'our',
    'this', 'that', 'what', 'who',
    # Common verbs
    'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had',
    'do', 'does', 'did', 'will', 'would', 'can', 'could', 'may', 'might',
    'must', 'shall', 'should', 'make', 'made', 'get', 'got', 'go', 'went',
    'come', 'came', 'see', 'saw', 'know', 'take', 'think', 'look', 'want',
    'use', 'find', 'give', 'tell', 'work', 'call', 'try', 'ask', 'need',
    'feel', 'seem', 'leave', 'put',
    # Common nouns & adjectives
    'time', 'year', 'day', 'way', 'man', 'thing', 'life', 'hand', 'part',
    'place', 'case', 'point', 'fact', 'good', 'new', 'first', 'last',
    'long', 'great', 'little', 'own', 'other', 'old', 'right', 'big',
    'high', 'small', 'large', 'next', 'early', 'young', 'few', 'public',
    'bad', 'same', 'able',
    # Prepositions & conjunctions
    'in', 'on', 'at', 'to', 'for', 'of', 'with', 'from', 'by', 'about',
    'like', 'through', 'over', 'before', 'between', 'under', 'since',
    'without', 'and', 'or', 'but', 'if', 'than', 'because', 'as', 'until',
    'while', 'so', 'though', 'both', 'each', 'when', 'where', 'why', 'how',
    # Common adverbs
    'not', 'now', 'just', 'more', 'also', 'here', 'there', 'then', 'only',
    'very', 'well', 'back', 'still', 'even', 'much', 'too', 'such',
    'never', 'again', 'most', 'once', 'off', 'away', 'down', 'out', 'up',
    # Tech/common words
    'test', 'code', 'data', 'file', 'line', 'text', 'word', 'number',
    'system', 'program', 'set', 'run', 'value', 'name', 'type', 'state',
    'end', 'start',
]


def generate_lorem_ipsum(target_tokens: int) -> str:
    """Generate lorem ipsum text for given token count.

    Args:
        target_tokens: Number of tokens to generate (capped at 500,000)

    Returns:
        Generated lorem ipsum text
    """
    # Cap at 500k tokens for safety
    target_tokens = min(target_tokens, 500_000)

    tokens = 0
    result = ''

    while tokens < target_tokens:
        sentence_length = 10 + int(random.random() * 11)
        words_in_sentence = 0

        for i in range(sentence_length):
            if tokens >= target_tokens:
                break

            word = ONE_TOKEN_WORDS[int(random.random() * len(ONE_TOKEN_WORDS))]
            result += word
            tokens += 1
            words_in_sentence += 1

            if i == sentence_length - 1 or tokens >= target_tokens:
                result += '. '
            else:
                result += ' '

        if words_in_sentence > 0 and random.random() < 0.2 and tokens < target_tokens:
            result += '\n\n'

    return result.strip()


def get_prompt(args: str = '') -> list[dict[str, Any]]:
    """Get lorem ipsum skill prompt."""
    parsed = 0
    if args.strip():
        try:
            parsed = int(args)
        except ValueError:
            pass

    if args and (parsed <= 0):
        return [{'type': 'text', 'text': 'Invalid token count. Please provide a positive number (e.g., /lorem-ipsum 10000).'}]

    target_tokens = parsed if parsed > 0 else 10000
    capped_tokens = min(target_tokens, 500_000)

    if capped_tokens < target_tokens:
        text = f'Requested {target_tokens} tokens, but capped at 500,000 for safety.\n\n{generate_lorem_ipsum(capped_tokens)}'
    else:
        text = generate_lorem_ipsum(capped_tokens)

    return [{'type': 'text', 'text': text}]


def register() -> None:
    """Register the lorem-ipsum skill (ANT-only)."""
    if not is_ant_user():
        return

    register_bundled_skill(BundledSkillDefinition(
        name='lorem-ipsum',
        description='Generate filler text for long context testing.',
        argument_hint='[token_count]',
        user_invocable=True,
        get_prompt_for_command=get_prompt,
    ))