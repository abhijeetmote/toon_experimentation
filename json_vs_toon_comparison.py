#!/usr/bin/env python3
"""
JSON vs TOON Token Count Comparison for LLMs

This script compares JSON and TOON (Token-Oriented Object Notation) formats 
to determine which uses fewer tokens when used with Large Language Models (LLMs).

TOON is specifically designed for LLM prompts to reduce token usage by eliminating
redundant syntax found in JSON.

Created by: Abhijeet Mote
Email: abhijeetmote@gmail.com
LinkedIn: https://www.linkedin.com/in/abhijeet-mote/
"""

import tiktoken
import os
import argparse


def count_tokens(text: str, model: str = "gpt-4") -> int:
    """Count tokens using tiktoken for a given model."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        # Fallback to cl100k_base if model not found
        try:
            encoding = tiktoken.get_encoding(model)
        except KeyError:
            encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(text))


def read_file(filepath: str) -> str:
    """Read file content."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def main():
    """Main comparison function."""
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description="Compare JSON and TOON formats for token usage in LLMs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python json_vs_toon_comparison.py -j example.json -t example.toon
  python json_vs_toon_comparison.py --json example_large.json --toon example_large.toon
  python json_vs_toon_comparison.py -j example_nested.json -t example_nested.toon
        """
    )
    parser.add_argument(
        "-j", "--json",
        required=True,
        help="Path to JSON file"
    )
    parser.add_argument(
        "-t", "--toon",
        required=True,
        help="Path to TOON file"
    )
    
    args = parser.parse_args()
    
    json_file = args.json
    toon_file = args.toon
    
    print("=" * 80)
    print("JSON vs TOON Token Count Comparison for LLMs")
    print("=" * 80)
    print()
    
    try:
        json_str = read_file(json_file)
        toon_str = read_file(toon_file)
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        print(f"\nPlease ensure both {json_file} and {toon_file} files exist.")
        print("\nUsage: python json_vs_toon_comparison.py -j JSON_FILE -t TOON_FILE")
        return
    
    # Count tokens for different models
    # Note: GPT-5 is not yet available. Adding latest available models.
    models = [
        "gpt-4",
        "gpt-4-turbo",
        "gpt-4o",  # Latest GPT-4 variant
        "gpt-3.5-turbo",
        "o1-preview",
        "o1-mini",
        "cl100k_base",  # Base encoding used by GPT-3.5 and GPT-4
        "o200k_base",  # Encoding used by o1 models
    ]
    
    print("Format Comparison:")
    print("-" * 80)
    print(f"JSON size: {len(json_str):,} characters")
    print(f"TOON size: {len(toon_str):,} characters")
    print(f"Size difference: {len(json_str) - len(toon_str):+,} characters")
    print()
    
    print("Token Count Comparison:")
    print("-" * 80)
    
    results = []
    successful_models = []
    
    for model in models:
        try:
            json_tokens = count_tokens(json_str, model)
            toon_tokens = count_tokens(toon_str, model)
            difference = json_tokens - toon_tokens
            percentage_diff = (difference / json_tokens) * 100 if json_tokens > 0 else 0
            
            results.append({
                "model": model,
                "json_tokens": json_tokens,
                "toon_tokens": toon_tokens,
                "difference": difference
            })
            successful_models.append(model)
            
            print(f"\nModel: {model}")
            print(f"  JSON tokens:  {json_tokens:,}")
            print(f"  TOON tokens:  {toon_tokens:,}")
            print(f"  Difference:   {difference:+,} tokens ({percentage_diff:+.2f}%)")
            
            if difference > 0:
                print(f"  ✅ TOON uses {difference:,} fewer tokens ({percentage_diff:.2f}% savings)")
            elif difference < 0:
                print(f"  ✅ JSON uses {abs(difference):,} fewer tokens ({abs(percentage_diff):.2f}% savings)")
            else:
                print(f"  ⚖️  Both formats use the same number of tokens")
        except Exception as e:
            print(f"\nModel: {model}")
            print(f"  ⚠️  Could not process: {str(e)}")
    
    print()
    print("=" * 80)
    print("Detailed Format Samples (first 500 chars):")
    print("=" * 80)
    print()
    
    print("JSON Sample:")
    print("-" * 80)
    print(json_str[:500] + "..." if len(json_str) > 500 else json_str)
    print()
    
    print("TOON Sample:")
    print("-" * 80)
    print(toon_str[:500] + "..." if len(toon_str) > 500 else toon_str)
    print()
    
    # Summary
    print()
    print("=" * 80)
    print("Summary:")
    print("-" * 80)
    if results:
        avg_json = sum(r["json_tokens"] for r in results) / len(results)
        avg_toon = sum(r["toon_tokens"] for r in results) / len(results)
        avg_diff = avg_json - avg_toon
        
        print(f"Models tested: {len(successful_models)}")
        print(f"Average JSON tokens:  {avg_json:,.0f}")
        print(f"Average TOON tokens:  {avg_toon:,.0f}")
        print(f"Average difference:   {avg_diff:+,.0f} tokens")
        
        if avg_diff > 0:
            print(f"\n🎯 Recommendation: Use TOON (saves ~{avg_diff:.0f} tokens on average)")
        elif avg_diff < 0:
            print(f"\n🎯 Recommendation: Use JSON (saves ~{abs(avg_diff):.0f} tokens on average)")
        else:
            print(f"\n🎯 Recommendation: Both formats are equivalent in token usage")
        
        # Show best savings
        if results:
            best_savings = max(results, key=lambda x: x["difference"])
            print(f"\n💡 Best savings: {best_savings['model']} - {best_savings['difference']:,} tokens ({best_savings['difference']/best_savings['json_tokens']*100:.2f}%)")
    
    print("=" * 80)
    print(f"\nFiles used:")
    print(f"  - {json_file}")
    print(f"  - {toon_file}")
    print("=" * 80)


if __name__ == "__main__":
    main()
