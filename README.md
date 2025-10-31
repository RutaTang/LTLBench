# LTLBench

This is the source code for the paper **_LTLBench: Towards Benchmarks for Evaluating Temporal Logic Reasoning in Large
Language Models_**.

It consists of both the code of the **Dataset Construction Pipeline** and the code of **the Experiments and Analyses**.

## Prerequisites

1. Download this repository;
2. Install the required packages by running `pip install -r requirements.txt`;
3. (Optional) Configure API keys and URLs:
   - Copy `.env.example` to `.env`: `cp .env.example .env`
   - Edit `.env` and set your configurations:
     - `OPENAI_API_KEY`: Your OpenAI API key (for evaluating OpenAI models)
     - `OLLAMA_URL`: Custom Ollama server URL (defaults to `http://localhost:11434`)
     - `DEEPSEEK_API_KEY`: Your Deepseek API key (for evaluating Deepseek models)
     - `ALIBABA_API_KEY`: Your Alibaba Cloud API key (for evaluating Alibaba Qwen models)
4. (Optional) Download [Ollama](https://ollama.com/) if you want to evaluate the models available on Ollama.

## Run the Pipeline to Generate the Dataset

1. Run the following command to generate LTLBench dataset:

```bash
python -m src.main generate -c 2000 -e 3 -l 3 -s 1
```

For the command above, `-c` is the number of formulas to generate, `-e` is the number of events, `-l` is the number of
operators, and `-s` is the random seed.

2. Run the following command to batch-generate additional datasets:

```bash
python -m src.main batch-generate -c 300 -e 2 -l 1,2,3,4,5,7,9 -s 1
```

or

```bash
python -m src.main batch-generate -c 300 -e 2,3,4,5,7,9 -l 2 -s 1
```

For the commands above, for both `-e` and `-l`, you can pass a comma-separated list of values for the number of events
and operators.

## Run the Experiments

**Note**: Before running the experiments, make sure to set your OpenAI API key in the `.env` file and also to download
Ollama
and pull the models you want.

### Prompt Strategies

LTLBench supports multiple prompt strategies to evaluate model performance:

- **`direct`**: Direct prompting without reasoning steps
- **`zero_shot_cot`**: Zero-shot Chain-of-Thought prompting
- **`few_shot_cot`**: Few-shot Chain-of-Thought with examples
- **`self_consistency`**: Self-consistency with multiple samples and majority voting
- **`least_to_most`**: Least-to-most prompting with problem decomposition

### Evaluation Commands

1. Run the following command to evaluate a model on the LTLBench dataset:

```bash
python -m src.main evaluate -c 2000 -e 3 -l 3 -m gpt-3.5-turbo -s direct
```

You can also specify different prompt strategies with the `-s` flag:

```bash
# Zero-shot Chain-of-Thought
python -m src.main evaluate -c 2000 -e 3 -l 3 -m gpt-4 -s zero_shot_cot

# Few-shot Chain-of-Thought
python -m src.main evaluate -c 2000 -e 3 -l 3 -m gpt-4 -s few_shot_cot

# Self-consistency (5 samples with majority voting)
python -m src.main evaluate -c 2000 -e 3 -l 3 -m gpt-4 -s self_consistency

# Least-to-most prompting
python -m src.main evaluate -c 2000 -e 3 -l 3 -m gpt-4 -s least_to_most
```

For the command above, you can change `gpt-3.5-turbo` to any other available model while you should also have a look at
the code in `src/models/choose.py` to see the available models. If you want to evaluate models not available in the
code, you can slightly modify the code to include them which should not be troublesome.

2. Run the following command to batch-evaluate a model on the LTLBench dataset:

```bash
python -m src.main batch-evaluate -c 300 -e 2 -l 1,2,3,4,5,7,9 -m gpt-3.5-turbo -s direct
```

You can also specify different prompt strategies for batch evaluation:

```bash
python -m src.main batch-evaluate -c 300 -e 2 -l 1,2,3,4,5,7,9 -m gpt-4 -s few_shot_cot
```





