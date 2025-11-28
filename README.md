# JSON vs TOON Token Count Comparison

This project compares JSON and TOON (Token-Oriented Object Notation) formats to determine which uses fewer tokens when used with Large Language Models (LLMs).

TOON is a compact, human-readable serialization format specifically designed for LLM prompts to reduce token usage by eliminating redundant syntax found in JSON.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python json_vs_toon_comparison.py -j <json_file> -t <toon_file>
```

**Arguments:**
- `-j, --json`: Path to JSON file (required)
- `-t, --toon`: Path to TOON file (required)

**Examples:**
```bash
# Compare small example files
python json_vs_toon_comparison.py -j example_datasets/example.json -t example_datasets/example.toon

# Compare large dataset
python json_vs_toon_comparison.py -j example_datasets/example_large.json -t example_datasets/example_large.toon

# Compare nested structures
python json_vs_toon_comparison.py -j example_datasets/example_nested.json -t example_datasets/example_nested.toon

# Compare deeply nested example
python json_vs_toon_comparison.py -j example_datasets/example_deeply_nested.json -t example_datasets/example_deeply_nested.toon
```

The script compares token counts across multiple LLM models: GPT-4, GPT-4-turbo, GPT-4o, GPT-3.5-turbo, o1-preview, o1-mini, and base encodings (cl100k_base, o200k_base).

## What It Does

The script:
1. Reads JSON and TOON format files (specified via command-line arguments)
2. Counts tokens for each format using tiktoken across multiple LLM models
3. Compares the results and shows:
   - Character count comparison
   - Token count comparison for each model
   - Percentage savings/difference
   - Sample outputs from both formats
   - Average statistics across all models
   - Best savings recommendation
4. Provides recommendations on which format to use based on the data structure

## Example Comparisons

### Example 1: Flat/Tabular Data (TOON Wins) ✅

**Small Dataset (3 products):**

*See `example.json` and `example.toon` for the actual files.*

**JSON (92-93 tokens):**
```json
{
  "products": [
    {
      "id": 1,
      "name": "Laptop",
      "price": 3999.90
    },
    {
      "id": 2,
      "name": "Mouse",
      "price": 149.90
    },
    {
      "id": 3,
      "name": "Headset",
      "price": 499.00
    }
  ]
}
```

**TOON (42 tokens):**
```toon
products[3]{id,name,price}:
  1,Laptop,3999.90
  2,Mouse,149.90
  3,Headset,499.00
```

**Result**: **54% token reduction with TOON** ✅

**Large Dataset (100 products with 10 fields including nested objects):**

*See `example_large.json` and `example_large.toon` for the actual files.*

- **JSON**: 17,109 tokens (57,741 characters, 2,703 lines)
- **TOON**: 6,433 tokens (15,556 characters, 100 lines)
- **Result**: **62.40% token reduction** - saves 10,676 tokens! ✅

**Cost Impact (100 products, 1,000 API calls at GPT-4 input pricing: $0.03 per 1K tokens):**
- JSON cost: ~$513 (17.1M tokens)
- TOON cost: ~$193 (6.4M tokens)
- **Total savings: ~$320 (62.4% reduction)**

*Note: Pricing based on GPT-4 input tokens. Actual costs may vary by model and region.*

*Note: This example includes more fields per product (id, name, category, price, stock, rating, description, tags, vendor info, specifications) compared to the simple example above, which demonstrates that TOON's efficiency improves with larger, more complex datasets.*

### Example 2: Deeply Nested Data (JSON Wins) ⚠️

*See `example_deeply_nested.json` and `example_deeply_nested.toon` for the actual files.*

**JSON (67 tokens - compact, no whitespace):**
```json
{"a":{"b":{"c":{"d":{"e":{"f":{"g":{"h":{"i":{"j":{"k":{"l":{"m":{"n":{"o":{"p":{"q":{"r":{"s":{"t":{"u":{"v":{"w":{"x":{"y":{"z":1}}}}}}}}}}}}}}}}}}}}}}}}}}
```

**TOON (80 tokens - indentation overhead):**
```toon
a:
  b:
    c:
      d:
        e:
          f:
            g:
              h:
                i:
                  j:
                    k:
                      l:
                        m:
                          n:
                            o:
                              p:
                                q:
                                  r:
                                    s:
                                      t:
                                        u:
                                          v:
                                            w:
                                              x:
                                                y:
                                                  z: 1
```

**Result**: **TOON uses 19% MORE tokens** ⚠️

### Example 3: Moderately Nested Product Data (TOON Still Wins) ✅

*See `example_nested.json` and `example_nested.toon` for the actual files.*

This example shows a product with nested details (specifications, marketing info, inventory):

- **JSON**: 197 tokens (723 characters)
- **TOON**: 135 tokens (497 characters)
- **Result**: **31.47% token reduction** - saves 62 tokens! ✅

*This demonstrates that moderate nesting (4-5 levels) still benefits from TOON, unlike extreme nesting (26+ levels) where JSON becomes more efficient.*

## Key Takeaways

### When TOON Excels ✅
- **Flat or tabular data** with uniform structure
- **Arrays of objects** with consistent fields
- **Large datasets** where header declaration pays off
- **API responses** with repeated structures

**Savings**: 30-60% token reduction, often improving LLM accuracy too.

### When JSON is Better ⚠️
- **Deeply nested structures** (5+ levels)
- **Inconsistent schemas** where fields vary per object
- **Compact JSON** (minified, no whitespace) for extreme nesting

**Strategy**: Flatten your JSON → convert to TOON → feed to LLMs for best results.

## About TOON

**TOON (Token-Oriented Object Notation)** is a serialization format designed specifically for LLM prompts. It achieves 30-60% token reduction compared to JSON by:

- Eliminating redundant syntax (braces, brackets, repeated keys)
- Using tabular format for uniform arrays of objects
- Declaring keys once and streaming data as rows
- Providing explicit array lengths and field headers for better LLM parsing

**Key Features:**
- ✅ **Compact Syntax** – Eliminates unnecessary punctuation and whitespace
- ✅ **Type Inference** – Automatically detects data types (numbers, booleans, null)
- ✅ **Array-First Design** – Optimized for tabular data and API responses
- ✅ **Human Readable** – Easy to read and understand, like CSV but more powerful
- ✅ **Privacy-First** – Conversions can be performed entirely client-side

**Learn more:**
- [TOON GitHub Repository](https://github.com/toon-format/toon)
- [TOON Specification](https://github.com/toon-format/toon/blob/main/SPEC.md)
- [TOON Documentation](https://toonformat.dev)

## Real-World Impact

For developers and organizations leveraging LLMs, TOON offers tangible benefits:

💰 **Cost Efficiency**: Direct reduction in API costs through lower token usage  
⚡ **Performance**: Faster processing times and more efficient context window usage  
🔒 **Privacy**: Client-side conversion ensures sensitive data stays private  
📊 **Scalability**: Better handling of large datasets and bulk operations

## Example Files

The project includes several example file pairs for testing:

- `example.json` / `example.toon` - Small products example (3 items, 3 fields: id, name, price)
- `example_large.json` / `example_large.toon` - Large products example (100 items, 10 fields including nested objects)
- `example_nested.json` / `example_nested.toon` - Nested product structure example (moderate nesting, 4-5 levels)
- `example_deeply_nested.json` / `example_deeply_nested.toon` - Extreme nesting example (26 levels deep)

## The Bottom Line

**TOON shines when the schema is consistent. JSON shines when the schema is deeply nested.**

This isn't about JSON vs TOON — it's about choosing the right format for the right shape of data. In production LLM pipelines, that choice can save you:
- Real money (30-60% cost reduction)
- Real latency (smaller payloads)
- Real model capacity (more data in context window)


