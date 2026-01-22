<div class="title-slide">
  
# Module 2.1 - Evaluation Frameworks and Tools   
<span style="font-size:20px; line-height:2;">
Dr. Hari Manassery Koduvely <br> 
Principal Data Scientist  <br>  
Cybersecurity Analytics <br>  
Ottawa, Canada <br>  
December 08, 2025

## How to Clone this Respository on your Work Laptop

- <span style="font-size:18px;">If your laptop do not have Git, install from https://github.com/git-guides/install-git</span>
- <span style="font-size:18px;">If your laptop do not have an IDE to open Jupyter Notebook install Vistual Studio Code from here https://code.visualstudio.com/download</span>
- <span style="font-size:18px;">To clone the repository:</span>
  - <span style="font-size:16px;">git clone https://github.com/harik68/Course-Evaluation-of-GenAI-Applications.git</span>
  - <span style="font-size:16px;">git clone https://github.com/harik68/Course-Evaluation-of-GenAI-Applications.git</span>
- <span style="font-size:18px;">Change directory to Course-Evaluation-of-GenAI-Applications/Session-1-Evaluation-Principles-and-Methods</span>
- <span style="font-size:18px;">Open the Jupyter Notebook Module1.1-Foundations-of-GenAI-Evaluation.ipynb using the IDE</span>

### Importing Libraries

```python
from typing import Dict
from collections import Counter
import pandas as pd
from IPython.display import Image, display
import textwrap
import os
import openai
from IPython.display import Image, display, HTML
from openai import OpenAI
```

## Quick Recap of Session 1

- <span style="font-size:18px;">**GenAI Application** evaluation is a Holistic Process.</span>
- <span style="font-size:18px;">**Reference-Based** and **Reference-Free** Evaluations.</span>
- <span style="font-size:18px;">**Classical Metrics** for Reference-Based Evaluations for Text Generation use cases.</span>
  - <span style="font-size:16px;">ROUGE</span>
  - <span style="font-size:16px;">BLEU</span>
  - <span style="font-size:16px;">METEOR</span>
  - <span style="font-size:16px;">BERT Score</span>
- <span style="font-size:18px;">**LLM-as-a-Judge** method</span>
  - <span style="font-size:16px;">Single output scoring without a reference.</span>
  - <span style="font-size:16px;">Single output scoring with a reference.</span>
  - <span style="font-size:16px;">Pairwise comparison.</span>
- <span style="font-size:18px;">LLM-as-a-Judge method **Prompt Guidelines**</span>
  - <span style="font-size:16px;">Discrete scores</span>
  - <span style="font-size:16px;">Rubrics</span>
- <span style="font-size:18px;">**Biases** in LLM-as-a-Judge method and their mitigations.</span>

[**Reference to Session 1 Jupyter Notebook**](./Module2.1-Evaluation-Frameworks-and-Tools.ipynb)

## Sesssion 2 Learning Objectives

- <span style="font-size:18px;"> What is **Observability** ?</span>
- <span style="font-size:18px;"> How to instrument Observability using **Open Telemetry**</span>
- <span style="font-size:18px;"> **G-Eval** Framework </span>
- <span style="font-size:18px;"> **RAGAS** Framework </span>

- <span style="font-size:18px;"> Open Source tool **DeepEval** </span>

- <span style="font-size:18px;"> **DAG Eval** Framework </span>

## Observability

- <span style="font-size:18px;">**External queries**: Ask about system behavior without needing internal knowledge.</span>
- <span style="font-size:18px;">**Faster troubleshooting**: Diagnose and resolve novel problems quickly.</span>
- <span style="font-size:18px;">**Behavior explanation**: Surface signals that reveal why something is happening.</span>

## Telemetry

- <span style="font-size:18px;">Data emitted from a system and its behavior.</span>
- <span style="font-size:18px;">Data comes in the form of signals: </span>
  - <span style="font-size:16px;">Spans </span>
  - <span style="font-size:16px;">Traces </span>
  - <span style="font-size:16px;">Metrics </span>
  - <span style="font-size:16px;">Logs </span>
- <span style="font-size:18px;">**Open Telemetry** - an open source **industry standard** for instrumenting observability. </span>

## Different Instrumentation Methodologies

<span style="font-size:18px;">**1.SDK-based (Decorators/Wrappers)**:</span>

- <span style="font-size:16px;">Mechanism: Developers manually wrap functions or use a vendor-specific SDK client.</span>

- <span style="font-size:16px;">Pros:</span>
  - <span style="font-size:16px;">Highest granularity.</span>
  - <span style="font-size:16px;">Allows capturing custom metadata and intermediate reasoning steps easily.</span>

- <span style="font-size:16px;">Cons:</span>
  - <span style="font-size:16px;">High code intrusion.</span>
  - <span style="font-size:16px;">Creates vendor lock-in.</span>

- <span style="font-size:16px;">Supporting Frameworks: LangSmith, Langfuse, MLflow.</span>

<span style="font-size:18px;">**2.Auto-Instrumentation using OpenTelemetry Standards (OTel)**:</span>

- <span style="font-size:16px;">Mechanism: **Monkey-patch** (replace original function with a wrapped function) a standard library (e.g ChatCompletion.create from OpenAI) at run time to:</span>
  - <span style="font-size:16px;">Emit traces.</span>
  - <span style="font-size:16px;">Calls the original API.</span>

- <span style="font-size:16px;">Pros:</span>
  - <span style="font-size:16px;">Minimal code changes (often just an initialization line @autotrace)</span>
  - <span style="font-size:16px;">Vendor-neutral (can switch backends easily)</span>
  - <span style="font-size:16px;">Compliant with industry standards.</span>

- <span style="font-size:16px;">Cons:
  - <span style="font-size:16px;">Could create conflict with other libraries.</span>
  - <span style="font-size:16px;">Less control over exactly what is logged compared to manual decorators.</span>

- <span style="font-size:16px;">Supporting Frameworks: OpenLLMetry, OpenLIT, Arize Phoenix.</span>

<span style="font-size:18px;">**3.Proxy-based**:</span>

- <span style="font-size:16px;">Mechanism: The application routes LLM requests through a middleware proxy server.</span>

- <span style="font-size:16px;">Pros:</span>
  - <span style="font-size:16px;">Zero overhead on the application.</span>
  - <span style="font-size:16px;">Language agnostic.</span>
  - <span style="font-size:16px;">Easiest to set up.</span>

- <span style="font-size:16px;">Cons:</span>
  - <span style="font-size:16px;"> "Black box" visibility (sees inputs/outputs but not internal app logic/retrieval steps)</span>
  - <span style="font-size:16px;"> Adds a network hop.</span>

- <span style="font-size:16px;">Supporting Frameworks: Helicone, MLflow AI Gateway.</span>

## What Does Observability Data Contains?

- <span style="font-size:20px;">Traces, which record the complete end-to-end journey of a request through the application.</span>

- <span style="font-size:20px;">Spans, each of which represent a single timed unit of work within a trace.</span>

### Spans

- <span style="font-size:18px;">**Unit of work**: represents a single request. </span>
- <span style="font-size:18px;">**Tracks** operations within a request.</span>
- <span style="font-size:18px;">**Reveals** what happened during execution.</span>
- <span style="font-size:18px;">**Open Telemetry Span Contains**:</span>
  - <span style="font-size:16px;">Name</span>
  - <span style="font-size:16px;">Parent Span ID</span>
  - <span style="font-size:16px;">Start and End Timestamps</span>
  - <span style="font-size:16px;">Span Context</span>
  - <span style="font-size:16px;">Attributes</span>
  - <span style="font-size:16px;">Span Events</span>
  - <span style="font-size:16px;">Span Links</span>
  - <span style="font-size:16px;">Span Status</span>

<div style='text-align: center;'>
    <img src='../Images/Span-Trace-Example.png' height='800'>
    <div style='font-size:16px; color:gray; margin-top:8px;'>
        Figure 1 A: An Example for a Span in Telemetry Data.<br>
        Reference: Open Telemetry Documentation.
    </div>
</div>

<div style='text-align: center;'>
    <img src='../Images/Span-Semantic-Conventions.png' height='500'>
    <div style='font-size:16px; color:gray; margin-top:8px;'>
        Figure 1 B: Span Semantic Conventions.<br>
        Reference: Open Telemetry Documentation.
    </div>
</div>

<div style='text-align: center;'>
    <img src='../Images/Span-Types.png' height='400'>
    <div style='font-size:16px; color:gray; margin-top:8px;'>
        Figure 1 C: Span Types.<br>
        Reference: Open Telemetry Documentation.
    </div>
</div>

### Traces

- <span style="font-size:18px;">The path of a request through the application. </span>
- <span style="font-size:18px;">Consists of multiple Spans.</span>
- <span style="font-size:18px;">Gives the full picture of end-to-end operations during a request.</span>

<div style='text-align: center;'>
    <img src='../Images/Trace-Fibonacci-Agent.png' height='800'>
    <div style='font-size:16px; color:gray; margin-top:8px;'>
        Figure 2: An Example for a Trace.<br>
    </div>
</div>

## Exercise 1: Hellow World Example for Tracing with OpenTelemetry

```python
%pip install opentracing
%pip install opentelemetry-sdk  -q
```

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, ConsoleSpanExporter

```

```python
provider = TracerProvider()
console_exporter = ConsoleSpanExporter()
provider.add_span_processor(SimpleSpanProcessor(console_exporter))
trace.set_tracer_provider(provider)
```

```python
tracer = trace.get_tracer("hello-world")
```

```python
import sys
import time
from tracing import init_tracer
import opentracing
tracer = opentracing.tracer
```

```python
def say_hello(hello_to):
    with tracer.start_as_current_span("say-hello") as span:
        span.set_attribute("hello-to", hello_to)
        hello_str = format_string(hello_to)
        print_hello(hello_str)

def format_string(hello_to):
    with tracer.start_as_current_span("format") as span:
        hello_str = f"Hello, {hello_to}!"
        span.add_event("string-format", {"value": hello_str})
        return hello_str

def print_hello(hello_str):
    with tracer.start_as_current_span("println") as span:
        print(hello_str)
        span.add_event("println")

```

```python
from pprint import pprint
pprint(say_hello("World"))
```

## Top Observability Frameworks

<div style='text-align: center;'>
    <img src='../Images/Top-Observability-Frameworks.png' height='500'>
    <div style='font-size:16px; color:gray; margin-top:8px;'>
        Figure 3: Comparison between Top Observability Frameworks.
    </div>
</div>

## Observability Frameworks in AWS Azure and GCP AI Studios

<div style='text-align: center;'>
    <img src='../Images/Observability-Comparison-AWS-GCP-Azure.png' height='550'>
    <div style='font-size:16px; color:gray; margin-top:8px;'>
        Figure 4: Comparison between Observability Frameworks in AWS AZure and GCP AI Studios.
    </div>
</div>

=================================================================================================================================================================

## G-Eval Framework

<div style='text-align: center;'>
    <img src='../Images/G-Eval-Framework.png' height='500'>
    <div style='font-size:16px; color:gray; margin-top:8px;'>
        Figure 5: G-Eval Publication.<br>
    </div>
</div>

-<span style="font-size:20px;">A structured approach to evaluate GenAI outputs on a Reference-free basis.</span>

-<span style="font-size:20px;">Combibes _Automatic Chain-of-Thought Reasoning_ and _Probability-Weighted Scoring_.</span>

-<span style="font-size:20px;">Achives better alignment with human judgements.</span>

<div style='text-align: center;'>
    <img src='../Images/High-Level-G-Eval-Framework.png' height='600'>
    <div style='font-size:16px; color:gray; margin-top:8px;'>
        Figure 5: G-Eval Overview.<br>
    </div>
</div>

<span style="font-size:18px;">**Step1**: Design a detailed natural languge prompt that explicitly define the evaluation task and criteria.</span>

<span style="font-size:18px;">**Step2**: Automatic Chain-of-Thought Generation.</span>

<span style="font-size:16px;">LLM generates it own detailed evaluation stepss based on the task and criteria.</span>

<span style="font-size:18px;">**Step3**: Calculation of Probability-weighted score.</span>  
<span style="font-size:20px;">

$$
score = \sum_{i=1}^{n} p(s_i)\space s_i
$$

</span>
<span style="font-size:16px;">Where $\{s_1, s_2, ..., s_n\}$ represents set of possible integer scores defined in the criteria.</span>   
  
<span style="font-size:16px;">And $p(s_i)$ is the probability of generating token $s_i$ by LLM.</span>

## RAGAS (Retrieval Augmented Generation Assessment) Framework

<span style="font-size:20px;">Retrieval Augmented Generation (RAG) is an efficient and cost-effective way to solve 3 main drawbacks of LLMs:</span>

- <span style="font-size:18px;">Lack of internal knowledge about events past their training cut-off date.</span>

- <span style="font-size:18px;">Lack of sufficient knowledge about highly specialized domains or company internal documents.</span>

- <span style="font-size:18px;">Prone to generating factually incorrect information.</span>

<div style='text-align: center;'>
    <img src='../Images/RAG-High-Level-Architecture.png' height='600'>
    <div style='font-size:16px; color:gray; margin-top:8px;'>
        Figure 6: RAG High-Level Architecture.<br>
        Reference: AWS RAG Documentation.
    </div>
</div>

<span style="font-size:20px;">Challenges in evaluation of RAG systems:</span>

- <span style="font-size:18px;">**Interplay of Components**: Quality of final answer depends on both the retriever and the generator.</span>

- <span style="font-size:18px;">**Lack of Universal Benchmarks**: No single benchmark dataset that applies to every RAG system.</span>

- <span style="font-size:18px;">**Dynamic Data and Drift**: Evaluation results can be outdated quickly when knowledge base get udated.</span>

- <span style="font-size:18px;">**Cost of Human Evaluation**: Frequent Human evaluation is time consuming and costly.</span>

<div style='text-align: center;'>
    <img src='../Images/RAGaS-Framework-Paper.png' height='600'>
    <div style='font-size:16px; color:gray; margin-top:8px;'>
        Figure 7: RAGAS Framework Paper.<br>
    </div>
</div>

<span style="font-size:20px;">RAGAS Introduced 3 core Metrics.</span>

<span style="font-size:20px;">1. **Faithfulness**: Measures whether claims in the generated answer can be supported by the retrieved context.</span>

- <span style="font-size:18px;">Direct measure of the degree of hallucination.</span>
- <span style="font-size:18px;">Judge-LLM extracts individual statements from the geneerated answer.</span>
- <span style="font-size:18px;">Verifies each statement against the context.</span>
- <span style="font-size:18px;">Faithfulness Score F is calculated as:</span>  
  <span style="font-size:18px;">
  $$
  F = \frac{V}{S}
  $$
  <span style="font-size:18px;"></span>
- <span style="font-size:18px;"> V - Number of verified statements.</span>
- <span style="font-size:18px;"> S - Number of total statements.</span>

<span style="font-size:20px;">2. **Answer Relevance**: Measures whether the generated response directly address the original question.</span>

- <span style="font-size:18px;">Judge-LLM first generate the potential questions the given answer could respond to.</span>
- <span style="font-size:18px;">Theen compute the average cosine similarity between generated questions and the original query</span>
- <span style="font-size:18px;">Answer Relevance Score AR is calculated as:</span>  
  <span style="font-size:18px;">

  $$
  AR = \frac{1}{n}\space \sum_{i=1}^{n}sim(q,q_i)
  $$

  <span style="font-size:18px;"></span>  
  <span style="font-size:20px;">2. **Context Relevance**: Measures how relevant the context is for answering the original question.</span>

- <span style="font-size:18px;">Judge-LLM extracts sentences from the context that are essential for answering the question.</span>
- <span style="font-size:18px;">Context Relevance Score CR is calculated as:</span>  
  <span style="font-size:18px;">
  $$
  CR = \frac{E}{S}
  $$
  <span style="font-size:18px;"></span>
- <span style="font-size:18px;"> E - Number of extracted sentences from context.</span>
- <span style="font-size:18px;"> S - Number of total sentences in context.</span>

## DeepEval Open-Source Evaluation Framework

- <span style="font-size:18px;"> Built on top of G-Eval framework.</span>

- <span style="font-size:18px;"> Plug-and-Use 30+ LLM-evaluated metrics.</span>

- <span style="font-size:18px;"> Supports both end-to-end and component level evaluation.</span>

- <span style="font-size:18px;"> Evaluation for RAG, Agents, Chatbots etc.</span>
- <span style="font-size:18px;"> Synthetic dataset generation capability.</span>
- <span style="font-size:18px;"> Customizable metrics.</span>
- <span style="font-size:18px;"> SecOps support for red teaming and safety scan for vulnerabilitites.</span>

### Plug-and-Use Metrics

<span style="font-size:22px;">1. Custom Metrics</span>

- <span style="font-size:18px;">G-Eval</span>
- <span style="font-size:18px;">Deep Acyclic Graph (DAG) Eval</span>

<span style="font-size:20px;">Example: Summarizaing Meeting Notes</span>

<span style="font-size:18px;">G-Eval:</span>

<span style="font-size:18px:"> A single prompt: <br>"Score is 0 if the summmary misses any of the headings: "intro", "body", "conclusion". <br> Score is 2 if the summary has all the 3 sections but are in the wrong order. <br>Score is 10 if the summary hasa all the 3 sections and they are in the correct order."</span>

<span style="font-size:18px;">DAG Eval:</span>

<div style='text-align: center;'>
    <img src='../Images/DeepEval-DAGEval.png' height='600'>
    <div style='font-size:16px; color:gray; margin-top:8px;'>
        Figure 8: DAG Eval Metric in DeepEval.<br>
        Reference: Deep Eval Documentation
    </div>
</div>

<span style="font-size:20px;">Advantages of DAG Eval over G-Eval</span>

- <span style="font-size:18px;">**Determinism**: Structured decision-tree approach ensures more consistent and reproducible results.</span>
- <span style="font-size:18px;">**Granular Control and Transparency**: Developers can define explicit sequence of checks to create a more auditable trail.</span>

- <span style="font-size:18px;">**Syntax and Structural Evaluations**: G-Eval struggles with strict structural checks such as "must have this JSON schema".</span>
- <span style="font-size:18px;">**Modular Design**: One can use G-Eval as a node within a DAG to leverage</span>
  - <span style="font-size:18px;">G-Eval's subjective strength.</span>
  - <span style="font-size:18px;">Deterministic conditions for structure and syntax.</span>

<span style="font-size:22px;"> 2. RAG Metrics</span>

<span style="font-size:20px;">Retriever Metrics:</span>

- <span style="font-size:18px;">Contextual Relevancy</span>
- <span style="font-size:18px;">Contextual Precision</span>

- <span style="font-size:18px;">Contextual Recall</span>

<span style="font-size:20px;">Generator Metrics:</span>

- <span style="font-size:18px;">Answer Relevancy</span>

- <span style="font-size:18px;">Faithfulness</span>

<span style="font-size:22px;"> 3. Agent Metrics</span>

- <span style="font-size:18px;">Task Completion</span>
- <span style="font-size:18px;">Tool Correctness</span>

<span style="font-size:22px;">4. Multi-Turn Chat Metrics</span>

- <span style="font-size:18px;">Knowledge Retention</span>
- <span style="font-size:18px;">Role Adherence</span>

- <span style="font-size:18px;">Conversation Completeness</span>

- <span style="font-size:18px;">Conversation Relevancy</span>

<span style="font-size:22px;">5. Multi-Modal Metrics</span>

- <span style="font-size:18px;">Image Coherence / Helpfulness / Reference</span>
- <span style="font-size:18px;">Text-to-Image</span>

- <span style="font-size:18px;">Multimodal Contextual Relevancy / Recall / Precision</span>

- <span style="font-size:18px;">Multimodal Answer Relevancy / Faithfulness</span>

<span style="font-size:22px;">6. Safety Metrics</span>

- <span style="font-size:18px;">Bias</span>
- <span style="font-size:18px;">Toxicity</span>

- <span style="font-size:18px;">Misuse</span>

- <span style="font-size:18px;">PII Leakage</span>

- <span style="font-size:18px;">Role Violation</span>

## Exercise 1

<span style="font-size:20px;">Perform evaluation of text summarization using G-Eval and DAG Eval.</span>

<span style="font-size:18px;">Installing DeepEval</span>

```python
!pip3 install --upgrade pip
!pip3 install --upgrade setuptools
!pip3 install --no-cache-dir grpcio
```

    Requirement already satisfied: pip in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (24.0)
    Collecting pip
    Collecting pip
      Downloading pip-25.3-py3-none-any.whl.metadata (4.7 kB)
      Downloading pip-25.3-py3-none-any.whl.metadata (4.7 kB)
    Downloading pip-25.3-py3-none-any.whl (1.8 MB)
    [2K   [91m━━━━━[0m[90m╺[0m[90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[0m [32m0.2/1.8 MB[0m [31m6.2 MB/s[0m eta [36m0:00:01[0mDownloading pip-25.3-py3-none-any.whl (1.8 MB)
    [2K   [90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[0m [32m1.8/1.8 MB[0m [31m8.2 MB/s[0m eta [36m0:00:00[0m00:01[0m00:01[0m
    [2K   [90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[0m [32m1.8/1.8 MB[0m [31m8.2 MB/s[0m eta [36m0:00:00[0m
    [?25hInstalling collected packages: pip
      Attempting uninstall: pip
    Installing collected packages: pip
      Attempting uninstall: pip
        Found existing installation: pip 24.0
        Uninstalling pip-24.0:
        Found existing installation: pip 24.0
        Uninstalling pip-24.0:
          Successfully uninstalled pip-24.0
          Successfully uninstalled pip-24.0
    Successfully installed pip-25.3
    Successfully installed pip-25.3

```python
%pip install deepeval==3.7.3
```

    Collecting deepeval==3.7.3
      Downloading deepeval-3.7.3-py3-none-any.whl.metadata (18 kB)
      Downloading deepeval-3.7.3-py3-none-any.whl.metadata (18 kB)
    Requirement already satisfied: aiohttp in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from deepeval==3.7.3) (3.9.5)
    Requirement already satisfied: anthropic in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from deepeval==3.7.3) (0.75.0)
    Requirement already satisfied: click<8.3.0,>=8.0.0 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from deepeval==3.7.3) (8.1.7)
    Requirement already satisfied: google-genai<2.0.0,>=1.9.0 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from deepeval==3.7.3) (1.53.0)
    Requirement already satisfied: grpcio<2.0.0,>=1.67.1 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from deepeval==3.7.3) (1.76.0)
    Requirement already satisfied: jinja2 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from deepeval==3.7.3) (3.1.4)
    Requirement already satisfied: nest_asyncio in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from deepeval==3.7.3) (1.6.0)
    Requirement already satisfied: ollama in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from deepeval==3.7.3) (0.6.1)
    Requirement already satisfied: openai in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from deepeval==3.7.3) (2.8.1)
    Requirement already satisfied: opentelemetry-api<2.0.0,>=1.24.0 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from deepeval==3.7.3) (1.39.0)
    Requirement already satisfied: opentelemetry-exporter-otlp-proto-grpc<2.0.0,>=1.24.0 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from deepeval==3.7.3) (1.39.0)
    Requirement already satisfied: opentelemetry-sdk<2.0.0,>=1.24.0 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from deepeval==3.7.3) (1.39.0)
    Requirement already satisfied: portalocker in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from deepeval==3.7.3) (3.2.0)
    Requirement already satisfied: aiohttp in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from deepeval==3.7.3) (3.9.5)
    Requirement already satisfied: anthropic in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from deepeval==3.7.3) (0.75.0)
    Requirement already satisfied: click<8.3.0,>=8.0.0 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from deepeval==3.7.3) (8.1.7)
    Requirement already satisfied: google-genai<2.0.0,>=1.9.0 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from deepeval==3.7.3) (1.53.0)
    Requirement already satisfied: grpcio<2.0.0,>=1.67.1 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from deepeval==3.7.3) (1.76.0)
    Requirement already satisfied: jinja2 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from deepeval==3.7.3) (3.1.4)
    Requirement already satisfied: nest_asyncio in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from deepeval==3.7.3) (1.6.0)
    Requirement already satisfied: ollama in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from deepeval==3.7.3) (0.6.1)
    Requirement already satisfied: openai in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from deepeval==3.7.3) (2.8.1)
    Requirement already satisfied: opentelemetry-api<2.0.0,>=1.24.0 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from deepeval==3.7.3) (1.39.0)
    Requirement already satisfied: opentelemetry-exporter-otlp-proto-grpc<2.0.0,>=1.24.0 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from deepeval==3.7.3) (1.39.0)
    Requirement already satisfied: opentelemetry-sdk<2.0.0,>=1.24.0 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from deepeval==3.7.3) (1.39.0)
    Requirement already satisfied: portalocker in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from deepeval==3.7.3) (3.2.0)
    Collecting posthog<6.0.0,>=5.4.0 (from deepeval==3.7.3)
      Using cached posthog-5.4.0-py3-none-any.whl.metadata (5.7 kB)
    Collecting posthog<6.0.0,>=5.4.0 (from deepeval==3.7.3)
      Using cached posthog-5.4.0-py3-none-any.whl.metadata (5.7 kB)
    Requirement already satisfied: pydantic<3.0.0,>=2.11.7 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from deepeval==3.7.3) (2.12.5)
    Requirement already satisfied: pydantic-settings<3.0.0,>=2.10.1 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from deepeval==3.7.3) (2.12.0)
    Requirement already satisfied: pyfiglet in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from deepeval==3.7.3) (1.0.4)
    Requirement already satisfied: pytest in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from deepeval==3.7.3) (9.0.2)
    Requirement already satisfied: pytest-asyncio in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from deepeval==3.7.3) (1.3.0)
    Requirement already satisfied: pytest-repeat in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from deepeval==3.7.3) (0.9.4)
    Requirement already satisfied: pytest-rerunfailures in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from deepeval==3.7.3) (12.0)
    Requirement already satisfied: pytest-xdist in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from deepeval==3.7.3) (3.8.0)
    Requirement already satisfied: python-dotenv<2.0.0,>=1.1.1 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from deepeval==3.7.3) (1.2.1)
    Requirement already satisfied: requests<3.0.0,>=2.31.0 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from deepeval==3.7.3) (2.32.2)
    Requirement already satisfied: rich<15.0.0,>=13.6.0 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from deepeval==3.7.3) (13.7.1)
    Requirement already satisfied: sentry-sdk in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from deepeval==3.7.3) (2.47.0)
    Requirement already satisfied: setuptools in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from deepeval==3.7.3) (80.9.0)
    Requirement already satisfied: tabulate<0.10.0,>=0.9.0 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from deepeval==3.7.3) (0.9.0)
    Requirement already satisfied: tenacity<=10.0.0,>=8.0.0 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from deepeval==3.7.3) (8.4.2)
    Requirement already satisfied: tqdm<5.0.0,>=4.66.1 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from deepeval==3.7.3) (4.66.4)
    Requirement already satisfied: typer<1.0.0,>=0.9 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from deepeval==3.7.3) (0.12.3)
    Requirement already satisfied: wheel in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from deepeval==3.7.3) (0.43.0)
    Requirement already satisfied: anyio<5.0.0,>=4.8.0 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from google-genai<2.0.0,>=1.9.0->deepeval==3.7.3) (4.12.0)
    Requirement already satisfied: google-auth<3.0.0,>=2.14.1 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from google-auth[requests]<3.0.0,>=2.14.1->google-genai<2.0.0,>=1.9.0->deepeval==3.7.3) (2.43.0)
    Requirement already satisfied: httpx<1.0.0,>=0.28.1 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from google-genai<2.0.0,>=1.9.0->deepeval==3.7.3) (0.28.1)
    Requirement already satisfied: websockets<15.1.0,>=13.0.0 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from google-genai<2.0.0,>=1.9.0->deepeval==3.7.3) (15.0.1)
    Requirement already satisfied: typing-extensions<5.0.0,>=4.11.0 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from google-genai<2.0.0,>=1.9.0->deepeval==3.7.3) (4.15.0)
    Requirement already satisfied: idna>=2.8 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from anyio<5.0.0,>=4.8.0->google-genai<2.0.0,>=1.9.0->deepeval==3.7.3) (3.7)
    Requirement already satisfied: cachetools<7.0,>=2.0.0 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from google-auth<3.0.0,>=2.14.1->google-auth[requests]<3.0.0,>=2.14.1->google-genai<2.0.0,>=1.9.0->deepeval==3.7.3) (6.2.2)
    Requirement already satisfied: pyasn1-modules>=0.2.1 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from google-auth<3.0.0,>=2.14.1->google-auth[requests]<3.0.0,>=2.14.1->google-genai<2.0.0,>=1.9.0->deepeval==3.7.3) (0.4.2)
    Requirement already satisfied: rsa<5,>=3.1.4 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from google-auth<3.0.0,>=2.14.1->google-auth[requests]<3.0.0,>=2.14.1->google-genai<2.0.0,>=1.9.0->deepeval==3.7.3) (4.9.1)
    Requirement already satisfied: certifi in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from httpx<1.0.0,>=0.28.1->google-genai<2.0.0,>=1.9.0->deepeval==3.7.3) (2024.6.2)
    Requirement already satisfied: httpcore==1.* in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from httpx<1.0.0,>=0.28.1->google-genai<2.0.0,>=1.9.0->deepeval==3.7.3) (1.0.5)
    Requirement already satisfied: h11<0.15,>=0.13 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from httpcore==1.*->httpx<1.0.0,>=0.28.1->google-genai<2.0.0,>=1.9.0->deepeval==3.7.3) (0.14.0)
    Requirement already satisfied: importlib-metadata<8.8.0,>=6.0 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from opentelemetry-api<2.0.0,>=1.24.0->deepeval==3.7.3) (7.1.0)
    Requirement already satisfied: zipp>=0.5 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from importlib-metadata<8.8.0,>=6.0->opentelemetry-api<2.0.0,>=1.24.0->deepeval==3.7.3) (3.17.0)
    Requirement already satisfied: pydantic<3.0.0,>=2.11.7 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from deepeval==3.7.3) (2.12.5)
    Requirement already satisfied: pydantic-settings<3.0.0,>=2.10.1 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from deepeval==3.7.3) (2.12.0)
    Requirement already satisfied: pyfiglet in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from deepeval==3.7.3) (1.0.4)
    Requirement already satisfied: pytest in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from deepeval==3.7.3) (9.0.2)
    Requirement already satisfied: pytest-asyncio in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from deepeval==3.7.3) (1.3.0)
    Requirement already satisfied: pytest-repeat in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from deepeval==3.7.3) (0.9.4)
    Requirement already satisfied: pytest-rerunfailures in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from deepeval==3.7.3) (12.0)
    Requirement already satisfied: pytest-xdist in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from deepeval==3.7.3) (3.8.0)
    Requirement already satisfied: python-dotenv<2.0.0,>=1.1.1 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from deepeval==3.7.3) (1.2.1)
    Requirement already satisfied: requests<3.0.0,>=2.31.0 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from deepeval==3.7.3) (2.32.2)
    Requirement already satisfied: rich<15.0.0,>=13.6.0 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from deepeval==3.7.3) (13.7.1)
    Requirement already satisfied: sentry-sdk in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from deepeval==3.7.3) (2.47.0)
    Requirement already satisfied: setuptools in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from deepeval==3.7.3) (80.9.0)
    Requirement already satisfied: tabulate<0.10.0,>=0.9.0 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from deepeval==3.7.3) (0.9.0)
    Requirement already satisfied: tenacity<=10.0.0,>=8.0.0 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from deepeval==3.7.3) (8.4.2)
    Requirement already satisfied: tqdm<5.0.0,>=4.66.1 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from deepeval==3.7.3) (4.66.4)
    Requirement already satisfied: typer<1.0.0,>=0.9 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from deepeval==3.7.3) (0.12.3)
    Requirement already satisfied: wheel in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from deepeval==3.7.3) (0.43.0)
    Requirement already satisfied: anyio<5.0.0,>=4.8.0 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from google-genai<2.0.0,>=1.9.0->deepeval==3.7.3) (4.12.0)
    Requirement already satisfied: google-auth<3.0.0,>=2.14.1 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from google-auth[requests]<3.0.0,>=2.14.1->google-genai<2.0.0,>=1.9.0->deepeval==3.7.3) (2.43.0)
    Requirement already satisfied: httpx<1.0.0,>=0.28.1 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from google-genai<2.0.0,>=1.9.0->deepeval==3.7.3) (0.28.1)
    Requirement already satisfied: websockets<15.1.0,>=13.0.0 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from google-genai<2.0.0,>=1.9.0->deepeval==3.7.3) (15.0.1)
    Requirement already satisfied: typing-extensions<5.0.0,>=4.11.0 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from google-genai<2.0.0,>=1.9.0->deepeval==3.7.3) (4.15.0)
    Requirement already satisfied: idna>=2.8 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from anyio<5.0.0,>=4.8.0->google-genai<2.0.0,>=1.9.0->deepeval==3.7.3) (3.7)
    Requirement already satisfied: cachetools<7.0,>=2.0.0 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from google-auth<3.0.0,>=2.14.1->google-auth[requests]<3.0.0,>=2.14.1->google-genai<2.0.0,>=1.9.0->deepeval==3.7.3) (6.2.2)
    Requirement already satisfied: pyasn1-modules>=0.2.1 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from google-auth<3.0.0,>=2.14.1->google-auth[requests]<3.0.0,>=2.14.1->google-genai<2.0.0,>=1.9.0->deepeval==3.7.3) (0.4.2)
    Requirement already satisfied: rsa<5,>=3.1.4 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from google-auth<3.0.0,>=2.14.1->google-auth[requests]<3.0.0,>=2.14.1->google-genai<2.0.0,>=1.9.0->deepeval==3.7.3) (4.9.1)
    Requirement already satisfied: certifi in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from httpx<1.0.0,>=0.28.1->google-genai<2.0.0,>=1.9.0->deepeval==3.7.3) (2024.6.2)
    Requirement already satisfied: httpcore==1.* in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from httpx<1.0.0,>=0.28.1->google-genai<2.0.0,>=1.9.0->deepeval==3.7.3) (1.0.5)
    Requirement already satisfied: h11<0.15,>=0.13 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from httpcore==1.*->httpx<1.0.0,>=0.28.1->google-genai<2.0.0,>=1.9.0->deepeval==3.7.3) (0.14.0)
    Requirement already satisfied: importlib-metadata<8.8.0,>=6.0 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from opentelemetry-api<2.0.0,>=1.24.0->deepeval==3.7.3) (7.1.0)
    Requirement already satisfied: zipp>=0.5 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from importlib-metadata<8.8.0,>=6.0->opentelemetry-api<2.0.0,>=1.24.0->deepeval==3.7.3) (3.17.0)
    Requirement already satisfied: googleapis-common-protos~=1.57 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from opentelemetry-exporter-otlp-proto-grpc<2.0.0,>=1.24.0->deepeval==3.7.3) (1.72.0)
    Requirement already satisfied: opentelemetry-exporter-otlp-proto-common==1.39.0 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from opentelemetry-exporter-otlp-proto-grpc<2.0.0,>=1.24.0->deepeval==3.7.3) (1.39.0)
    Requirement already satisfied: opentelemetry-proto==1.39.0 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from opentelemetry-exporter-otlp-proto-grpc<2.0.0,>=1.24.0->deepeval==3.7.3) (1.39.0)
    Requirement already satisfied: protobuf<7.0,>=5.0 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from opentelemetry-proto==1.39.0->opentelemetry-exporter-otlp-proto-grpc<2.0.0,>=1.24.0->deepeval==3.7.3) (6.33.2)
    Requirement already satisfied: opentelemetry-semantic-conventions==0.60b0 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from opentelemetry-sdk<2.0.0,>=1.24.0->deepeval==3.7.3) (0.60b0)
    Requirement already satisfied: six>=1.5 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from posthog<6.0.0,>=5.4.0->deepeval==3.7.3) (1.16.0)
    Requirement already satisfied: python-dateutil>=2.2 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from posthog<6.0.0,>=5.4.0->deepeval==3.7.3) (2.9.0)
    Requirement already satisfied: backoff>=1.10.0 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from posthog<6.0.0,>=5.4.0->deepeval==3.7.3) (2.2.1)
    Requirement already satisfied: distro>=1.5.0 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from posthog<6.0.0,>=5.4.0->deepeval==3.7.3) (1.9.0)
    Requirement already satisfied: annotated-types>=0.6.0 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from pydantic<3.0.0,>=2.11.7->deepeval==3.7.3) (0.7.0)
    Requirement already satisfied: pydantic-core==2.41.5 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from pydantic<3.0.0,>=2.11.7->deepeval==3.7.3) (2.41.5)
    Requirement already satisfied: typing-inspection>=0.4.2 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from pydantic<3.0.0,>=2.11.7->deepeval==3.7.3) (0.4.2)
    Requirement already satisfied: charset-normalizer<4,>=2 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from requests<3.0.0,>=2.31.0->deepeval==3.7.3) (3.3.2)
    Requirement already satisfied: urllib3<3,>=1.21.1 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from requests<3.0.0,>=2.31.0->deepeval==3.7.3) (2.2.1)
    Requirement already satisfied: markdown-it-py>=2.2.0 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from rich<15.0.0,>=13.6.0->deepeval==3.7.3) (3.0.0)
    Requirement already satisfied: pygments<3.0.0,>=2.13.0 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from rich<15.0.0,>=13.6.0->deepeval==3.7.3) (2.18.0)
    Requirement already satisfied: googleapis-common-protos~=1.57 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from opentelemetry-exporter-otlp-proto-grpc<2.0.0,>=1.24.0->deepeval==3.7.3) (1.72.0)
    Requirement already satisfied: opentelemetry-exporter-otlp-proto-common==1.39.0 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from opentelemetry-exporter-otlp-proto-grpc<2.0.0,>=1.24.0->deepeval==3.7.3) (1.39.0)
    Requirement already satisfied: opentelemetry-proto==1.39.0 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from opentelemetry-exporter-otlp-proto-grpc<2.0.0,>=1.24.0->deepeval==3.7.3) (1.39.0)
    Requirement already satisfied: protobuf<7.0,>=5.0 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from opentelemetry-proto==1.39.0->opentelemetry-exporter-otlp-proto-grpc<2.0.0,>=1.24.0->deepeval==3.7.3) (6.33.2)
    Requirement already satisfied: opentelemetry-semantic-conventions==0.60b0 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from opentelemetry-sdk<2.0.0,>=1.24.0->deepeval==3.7.3) (0.60b0)
    Requirement already satisfied: six>=1.5 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from posthog<6.0.0,>=5.4.0->deepeval==3.7.3) (1.16.0)
    Requirement already satisfied: python-dateutil>=2.2 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from posthog<6.0.0,>=5.4.0->deepeval==3.7.3) (2.9.0)
    Requirement already satisfied: backoff>=1.10.0 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from posthog<6.0.0,>=5.4.0->deepeval==3.7.3) (2.2.1)
    Requirement already satisfied: distro>=1.5.0 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from posthog<6.0.0,>=5.4.0->deepeval==3.7.3) (1.9.0)
    Requirement already satisfied: annotated-types>=0.6.0 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from pydantic<3.0.0,>=2.11.7->deepeval==3.7.3) (0.7.0)
    Requirement already satisfied: pydantic-core==2.41.5 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from pydantic<3.0.0,>=2.11.7->deepeval==3.7.3) (2.41.5)
    Requirement already satisfied: typing-inspection>=0.4.2 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from pydantic<3.0.0,>=2.11.7->deepeval==3.7.3) (0.4.2)
    Requirement already satisfied: charset-normalizer<4,>=2 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from requests<3.0.0,>=2.31.0->deepeval==3.7.3) (3.3.2)
    Requirement already satisfied: urllib3<3,>=1.21.1 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from requests<3.0.0,>=2.31.0->deepeval==3.7.3) (2.2.1)
    Requirement already satisfied: markdown-it-py>=2.2.0 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from rich<15.0.0,>=13.6.0->deepeval==3.7.3) (3.0.0)
    Requirement already satisfied: pygments<3.0.0,>=2.13.0 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from rich<15.0.0,>=13.6.0->deepeval==3.7.3) (2.18.0)
    Requirement already satisfied: pyasn1>=0.1.3 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from rsa<5,>=3.1.4->google-auth<3.0.0,>=2.14.1->google-auth[requests]<3.0.0,>=2.14.1->google-genai<2.0.0,>=1.9.0->deepeval==3.7.3) (0.6.1)
    Requirement already satisfied: shellingham>=1.3.0 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from typer<1.0.0,>=0.9->deepeval==3.7.3) (1.5.4)
    Requirement already satisfied: mdurl~=0.1 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from markdown-it-py>=2.2.0->rich<15.0.0,>=13.6.0->deepeval==3.7.3) (0.1.2)
    Requirement already satisfied: pyasn1>=0.1.3 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from rsa<5,>=3.1.4->google-auth<3.0.0,>=2.14.1->google-auth[requests]<3.0.0,>=2.14.1->google-genai<2.0.0,>=1.9.0->deepeval==3.7.3) (0.6.1)
    Requirement already satisfied: shellingham>=1.3.0 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from typer<1.0.0,>=0.9->deepeval==3.7.3) (1.5.4)
    Requirement already satisfied: mdurl~=0.1 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from markdown-it-py>=2.2.0->rich<15.0.0,>=13.6.0->deepeval==3.7.3) (0.1.2)
    Requirement already satisfied: aiosignal>=1.1.2 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from aiohttp->deepeval==3.7.3) (1.3.1)
    Requirement already satisfied: attrs>=17.3.0 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from aiohttp->deepeval==3.7.3) (23.2.0)
    Requirement already satisfied: frozenlist>=1.1.1 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from aiohttp->deepeval==3.7.3) (1.4.1)
    Requirement already satisfied: multidict<7.0,>=4.5 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from aiohttp->deepeval==3.7.3) (6.0.5)
    Requirement already satisfied: yarl<2.0,>=1.0 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from aiohttp->deepeval==3.7.3) (1.9.4)
    Requirement already satisfied: docstring-parser<1,>=0.15 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from anthropic->deepeval==3.7.3) (0.17.0)
    Requirement already satisfied: jiter<1,>=0.4.0 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from anthropic->deepeval==3.7.3) (0.12.0)
    Requirement already satisfied: sniffio in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from anthropic->deepeval==3.7.3) (1.3.1)
    Requirement already satisfied: MarkupSafe>=2.0 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from jinja2->deepeval==3.7.3) (2.1.5)
    Requirement already satisfied: aiosignal>=1.1.2 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from aiohttp->deepeval==3.7.3) (1.3.1)
    Requirement already satisfied: attrs>=17.3.0 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from aiohttp->deepeval==3.7.3) (23.2.0)
    Requirement already satisfied: frozenlist>=1.1.1 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from aiohttp->deepeval==3.7.3) (1.4.1)
    Requirement already satisfied: multidict<7.0,>=4.5 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from aiohttp->deepeval==3.7.3) (6.0.5)
    Requirement already satisfied: yarl<2.0,>=1.0 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from aiohttp->deepeval==3.7.3) (1.9.4)
    Requirement already satisfied: docstring-parser<1,>=0.15 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from anthropic->deepeval==3.7.3) (0.17.0)
    Requirement already satisfied: jiter<1,>=0.4.0 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from anthropic->deepeval==3.7.3) (0.12.0)
    Requirement already satisfied: sniffio in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from anthropic->deepeval==3.7.3) (1.3.1)
    Requirement already satisfied: MarkupSafe>=2.0 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from jinja2->deepeval==3.7.3) (2.1.5)
    Requirement already satisfied: iniconfig>=1.0.1 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from pytest->deepeval==3.7.3) (2.3.0)
    Requirement already satisfied: packaging>=22 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from pytest->deepeval==3.7.3) (24.0)
    Requirement already satisfied: pluggy<2,>=1.5 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from pytest->deepeval==3.7.3) (1.6.0)
    Requirement already satisfied: execnet>=2.1 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from pytest-xdist->deepeval==3.7.3) (2.1.2)
    Requirement already satisfied: iniconfig>=1.0.1 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from pytest->deepeval==3.7.3) (2.3.0)
    Requirement already satisfied: packaging>=22 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from pytest->deepeval==3.7.3) (24.0)
    Requirement already satisfied: pluggy<2,>=1.5 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from pytest->deepeval==3.7.3) (1.6.0)
    Requirement already satisfied: execnet>=2.1 in /Users/harikoduvely/miniconda3/envs/llm_env/lib/python3.11/site-packages (from pytest-xdist->deepeval==3.7.3) (2.1.2)
    Downloading deepeval-3.7.3-py3-none-any.whl (727 kB)
    [?25l   [90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[0m [32m0.0/727.3 kB[0m [31m?[0m eta [36m-:--:--[0mDownloading deepeval-3.7.3-py3-none-any.whl (727 kB)
    [2K   [90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[0m [32m727.3/727.3 kB[0m [31m6.5 MB/s[0m  [33m0:00:00[0m
    [?25hUsing cached posthog-5.4.0-py3-none-any.whl (105 kB)
    [2K   [90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[0m [32m727.3/727.3 kB[0m [31m6.5 MB/s[0m  [33m0:00:00[0m
    [?25hUsing cached posthog-5.4.0-py3-none-any.whl (105 kB)
    Installing collected packages: posthog, deepeval
    [2K  Attempting uninstall: posthog
    [2K    Found existing installation: posthog 6.9.3
    [2K    Uninstalling posthog-6.9.3:
    [2K      Successfully uninstalled posthog-6.9.3
    Installing collected packages: posthog, deepeval
    [2K  Attempting uninstall: posthog
    [2K    Found existing installation: posthog 6.9.3
    [2K    Uninstalling posthog-6.9.3:
    [2K      Successfully uninstalled posthog-6.9.3
    [2K  Attempting uninstall: deepeval━━━━━━━━━━━━━━━━[0m [32m0/2[0m [posthog]
    [2K    Found existing installation: deepeval 3.6.9m [32m0/2[0m [posthog]
    [2K  Attempting uninstall: deepeval━━━━━━━━━━━━[0m [32m0/2[0m [posthog]
    [2K    Found existing installation: deepeval 3.6.9m [32m0/2[0m [posthog]
    [2K    Uninstalling deepeval-3.6.9:[90m╺[0m[90m━━━━━━━━━━━━━━━━━━━[0m [32m1/2[0m [deepeval]
    [2K    Uninstalling deepeval-3.6.9:[90m╺[0m[90m━━━━━━━━━━━━━━━━━━━[0m [32m1/2[0m [deepeval]
    [2K      Successfully uninstalled deepeval-3.6.9━━━━━━━━━━━━━━━━━[0m [32m1/2[0m [deepeval]
    [2K      Successfully uninstalled deepeval-3.6.9━━━━━━━━━━━━━━━━━[0m [32m1/2[0m [deepeval]
    [2K   [90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[0m [32m2/2[0m [deepeval]1/2[0m [deepeval]
    [1A[2KSuccessfully installed deepeval-3.7.3 posthog-5.4.0
    [2K   [90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[0m [32m2/2[0m [deepeval]
    [1A[2KSuccessfully installed deepeval-3.7.3 posthog-5.4.0
    Note: you may need to restart the kernel to use updated packages.
    Note: you may need to restart the kernel to use updated packages.

**IMPORTANT: Restart the Kernel after installing deepeval before proceeding further**

<span style="font-size:18px;">Import Libraries</span>

```python
import os
from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCase,LLMTestCaseParams
from deepeval import evaluate
```

<span style="font-size:18px;">Setting up Open AI API for LLM</span>

```python
#os.environ["OPENAI_API_KEY"] = "your_api_key_here"  # Replace with your actual API key
```

```python
# Initialize the client
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)
```

```python
# Load the train data
df_train = pd.read_csv('../Data-Summarization/train_sample.csv')
article_text = df_train.loc[0, 'article']
```

```python
def generate_summarization_prompt(article_text: str, summary_length: int = 100) -> str:
    """
    Generates a prompt for text summarization to send to the OpenAI API.

    Args:
        article_text (str): The input article or document to summarize.
        summary_length (int): Desired length of the summary in words (default: 100).

    Returns:
        str: The formatted prompt for the OpenAI API.
    """
    prompt = (
        f"Summarize the following article in about {summary_length} words:\n\n"
        f"Article:\n{article_text}\n\n"
        "Summary:"
    )
    return prompt
```

```python
def get_chatgpt_response(prompt, model="gpt-4.1-mini"):
    """
    Sends a query to ChatGPT API and returns the model's response text.

    Args:
        prompt (str): The question or instruction for the model.
        model (str): Model name to use (default: "gpt-4.1-mini").

    Returns:
        str: The text output from ChatGPT.
    """
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    # Extract the message text
    return response.choices[0].message.content
```

<span style="font-size:18px;">Generate Prompt for Summarization</span>

```python
summary_length = 200
prompt = generate_summarization_prompt(article_text, summary_length)
print(textwrap.fill(prompt, width=100))
```

    Summarize the following article in about 200 words:  Article: A woman in the Northwest Highlands of
    Scotland who'd fallen ill tested negative for Ebola, the Scottish government said Tuesday. A
    spokesman for the government said the woman had been in West Africa recently, though she had no
    direct contact with anyone with Ebola. "A patient at Aberdeen Royal Infirmary has tested negative
    for Ebola," the press release said. "The individual was transferred to the hospital by the Scottish
    Ambulance Service yesterday after falling ill while visiting Torridon in the Scottish Highlands."
    Meanwhile, a health care worker who was diagnosed with the Ebola virus after returning to Scotland
    from Sierra Leone was transferred to the Royal Free Hospital in London. The patient is Pauline
    Cafferkey, 39, of Glasgow, Scotland, the hospital said. She was working with Save the Children at an
    Ebola treatment center, said Michael von Bertele, humanitarian director at that organization. She
    traveled via Casablanca, Morocco, and London Heathrow Airport before arriving at Glasgow Airport on
    a British Airways flight late Sunday, the health agency NHS Scotland said. After feeling unwell, she
    sought medical attention and became the first person to be diagnosed with Ebola within the United
    Kingdom. British media outlets said Cafferkey is a public health nurse in Scotland's South
    Lanarkshire area who was part of a 30-strong team of medical volunteers deployed to West Africa by
    the UK government last month in a joint endeavor with Save the Children. She was reportedly
    transferred to London in a military aircraft fitted with an isolation pod. The Royal Free Hospital
    is equipped with a high-level isolation unit, with access restricted to specially trained medical
    staff. A specially designed tent, with controlled ventilation, is set up over the patient's bed. A
    British volunteer nurse, William Pooley, was successfully treated in the unit after he was brought
    home from Sierra Leone in August, having been diagnosed with Ebola there. 'Extremely low' risk . UK
    authorities are working to trace those who have come into contact with Cafferkey. The Scottish
    government has set up a special number for people to call if they traveled on the same London
    Heathrow-to-Glasgow flight as Cafferkey. British Airways said it was working closely with health
    authorities in England and Scotland and would help with any information needed. "The safety and
    security of our customers and crew is always our top priority and the risk to people on board that
    individual flight is extremely low," the airline said. Ebola patients become infectious only after
    they display symptoms, such as fever and vomiting. The deadly virus is spread through contact with
    bodily fluids. A Downing Street spokesman told CNN that British Prime Minister David Cameron and
    Scottish First Minister Nicola Sturgeon had discussed the procedures in place to handle such a case.
    "They agreed that both governments would remain in close touch and ensure everything possible was
    done to support the patient and, although the risk to the general population remained low, all
    measures would be taken to protect public health." Possible case . Another suspected Ebola case is
    being tested in southwest England at the Royal Cornwall Hospital, health officials said. "We do not
    expect the results to be known for at least 24 hours and in the meantime the patient is being looked
    after in isolation, following nationally agreed guidelines and protocols to protect the health of
    our staff and other patients," said a joint statement from the hospital and Public Health England, a
    government agency. According to UK government guidelines, humanitarian workers returning from Ebola-
    affected countries in West Africa who've been at high risk of exposure are expected to monitor their
    own health for 21 days after they get home. As of December 24, at least 7,693 people had died in the
    current Ebola outbreak, centered in Liberia, Sierra Leone and Guinea, the World Health Organization
    said. There have been at least 19,695 cases.  Summary:

<span style="font-size:18px;">Generate Summary Using OpenAI API</span>

```python
model = "gpt-3.5-turbo"
generated_summary = get_chatgpt_response(prompt, model)
```

```python
print(textwrap.fill(generated_summary, width=100))
```

    A woman in the Northwest Highlands of Scotland tested negative for Ebola after falling ill, despite
    recently visiting West Africa. However, a health care worker named Pauline Cafferkey was diagnosed
    with Ebola after returning from Sierra Leone and was transferred to a hospital in London. Cafferkey
    had traveled via Casablanca and London before arriving in Scotland, where she sought medical
    attention. The Royal Free Hospital in London has a high-level isolation unit where Cafferkey was
    treated. UK authorities are working to trace those who came into contact with her, and another
    suspected Ebola case is being tested at a hospital in southwest England. As of December 24, there
    have been at least 7,693 deaths in the current Ebola outbreak in Liberia, Sierra Leone, and Guinea.
    The UK government guidelines require humanitarian workers returning from Ebola-affected countries to
    monitor their health for 21 days. Prime Minister David Cameron and First Minister Nicola Sturgeon
    have discussed measures to handle the cases and protect public health.

<span style="font-size:18px;">Run G-Eval</span>

```python
# Define the G-Eval metric for coherence, specifying the judge model
# Note: "gpt-4.1-mini" is a placeholder name used in documentation snippets; use "gpt-4-turbo" or the actual available model name.
# If "gpt-4.1-mini" is unavailable, the code might require adjustment to a valid model name.
coherence_metric_g_eval = GEval(
    name="Coherence",
    criteria="The summary must be well-structured and well-organized, building from sentence to sentence to a coherent body of information.",
    model = "gpt-4.1-mini",
    threshold=0.7,
    evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT],
    strict_mode=False
)

# Create a test case
test_case_g_eval = LLMTestCase(
    input=article_text,
    actual_output=generated_summary
)

# Evaluate using G-Eval
print("--- Running G-Eval ---")
g_eval_result = evaluate([test_case_g_eval], [coherence_metric_g_eval])

```

    --- Running G-Eval ---

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace">✨ You're running DeepEval's latest <span style="color: #6a00ff; text-decoration-color: #6a00ff">Coherence </span><span style="color: #6a00ff; text-decoration-color: #6a00ff; font-weight: bold">[</span><span style="color: #6a00ff; text-decoration-color: #6a00ff">GEval</span><span style="color: #6a00ff; text-decoration-color: #6a00ff; font-weight: bold">]</span><span style="color: #6a00ff; text-decoration-color: #6a00ff"> Metric</span>! <span style="color: #374151; text-decoration-color: #374151; font-weight: bold">(</span><span style="color: #374151; text-decoration-color: #374151">using gpt-</span><span style="color: #374151; text-decoration-color: #374151; font-weight: bold">4.1</span><span style="color: #374151; text-decoration-color: #374151">-mini, </span><span style="color: #374151; text-decoration-color: #374151">strict</span><span style="color: #374151; text-decoration-color: #374151">=</span><span style="color: #374151; text-decoration-color: #374151; font-style: italic">False</span><span style="color: #374151; text-decoration-color: #374151">, </span>
<span style="color: #374151; text-decoration-color: #374151">async_mode</span><span style="color: #374151; text-decoration-color: #374151">=</span><span style="color: #374151; text-decoration-color: #374151; font-style: italic">True</span><span style="color: #374151; text-decoration-color: #374151; font-weight: bold">)</span><span style="color: #374151; text-decoration-color: #374151">...</span>
</pre>

    Output()

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace"></pre>

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace">
</pre>

    ======================================================================

    Metrics Summary

      - ✅ Coherence [GEval] (score: 0.8182425532696179, threshold: 0.7, strict: False, evaluation model: gpt-4.1-mini, reason: The summary maintains a clear and logical flow, progressing from the negative test of the woman in Scotland to the confirmed Ebola case of Pauline Cafferkey, then to the hospital treatment and public health responses. It captures key points such as Cafferkey's travel, treatment, contact tracing, and government actions in a well-organized manner without abrupt jumps. The summary avoids redundancy and irrelevant details, though it omits some specifics like the involvement of Save the Children and the detailed description of the isolation unit, which slightly reduces completeness but does not harm coherence., error: None)

    For test case:

      - input: A woman in the Northwest Highlands of Scotland who'd fallen ill tested negative for Ebola, the Scottish government said Tuesday. A spokesman for the government said the woman had been in West Africa recently, though she had no direct contact with anyone with Ebola. "A patient at Aberdeen Royal Infirmary has tested negative for Ebola," the press release said. "The individual was transferred to the hospital by the Scottish Ambulance Service yesterday after falling ill while visiting Torridon in the Scottish Highlands." Meanwhile, a health care worker who was diagnosed with the Ebola virus after returning to Scotland from Sierra Leone was transferred to the Royal Free Hospital in London. The patient is Pauline Cafferkey, 39, of Glasgow, Scotland, the hospital said. She was working with Save the Children at an Ebola treatment center, said Michael von Bertele, humanitarian director at that organization. She traveled via Casablanca, Morocco, and London Heathrow Airport before arriving at Glasgow Airport on a British Airways flight late Sunday, the health agency NHS Scotland said. After feeling unwell, she sought medical attention and became the first person to be diagnosed with Ebola within the United Kingdom. British media outlets said Cafferkey is a public health nurse in Scotland's South Lanarkshire area who was part of a 30-strong team of medical volunteers deployed to West Africa by the UK government last month in a joint endeavor with Save the Children. She was reportedly transferred to London in a military aircraft fitted with an isolation pod. The Royal Free Hospital is equipped with a high-level isolation unit, with access restricted to specially trained medical staff. A specially designed tent, with controlled ventilation, is set up over the patient's bed. A British volunteer nurse, William Pooley, was successfully treated in the unit after he was brought home from Sierra Leone in August, having been diagnosed with Ebola there. 'Extremely low' risk . UK authorities are working to trace those who have come into contact with Cafferkey. The Scottish government has set up a special number for people to call if they traveled on the same London Heathrow-to-Glasgow flight as Cafferkey. British Airways said it was working closely with health authorities in England and Scotland and would help with any information needed. "The safety and security of our customers and crew is always our top priority and the risk to people on board that individual flight is extremely low," the airline said. Ebola patients become infectious only after they display symptoms, such as fever and vomiting. The deadly virus is spread through contact with bodily fluids. A Downing Street spokesman told CNN that British Prime Minister David Cameron and Scottish First Minister Nicola Sturgeon had discussed the procedures in place to handle such a case. "They agreed that both governments would remain in close touch and ensure everything possible was done to support the patient and, although the risk to the general population remained low, all measures would be taken to protect public health." Possible case . Another suspected Ebola case is being tested in southwest England at the Royal Cornwall Hospital, health officials said. "We do not expect the results to be known for at least 24 hours and in the meantime the patient is being looked after in isolation, following nationally agreed guidelines and protocols to protect the health of our staff and other patients," said a joint statement from the hospital and Public Health England, a government agency. According to UK government guidelines, humanitarian workers returning from Ebola-affected countries in West Africa who've been at high risk of exposure are expected to monitor their own health for 21 days after they get home. As of December 24, at least 7,693 people had died in the current Ebola outbreak, centered in Liberia, Sierra Leone and Guinea, the World Health Organization said. There have been at least 19,695 cases.
      - actual output: A woman in the Northwest Highlands of Scotland tested negative for Ebola after falling ill, despite recently visiting West Africa. However, a health care worker named Pauline Cafferkey was diagnosed with Ebola after returning from Sierra Leone and was transferred to a hospital in London. Cafferkey had traveled via Casablanca and London before arriving in Scotland, where she sought medical attention. The Royal Free Hospital in London has a high-level isolation unit where Cafferkey was treated. UK authorities are working to trace those who came into contact with her, and another suspected Ebola case is being tested at a hospital in southwest England. As of December 24, there have been at least 7,693 deaths in the current Ebola outbreak in Liberia, Sierra Leone, and Guinea. The UK government guidelines require humanitarian workers returning from Ebola-affected countries to monitor their health for 21 days. Prime Minister David Cameron and First Minister Nicola Sturgeon have discussed measures to handle the cases and protect public health.
      - expected output: None
      - context: None
      - retrieval context: None

    ======================================================================

    Overall Metric Pass Rates

    Coherence [GEval]: 100.00% pass rate

    ======================================================================

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace">
<span style="color: #808000; text-decoration-color: #808000; font-weight: bold">⚠ WARNING:</span> No hyperparameters logged.
» <a href="https://deepeval.com/docs/evaluation-prompts" target="_blank"><span style="color: #000080; text-decoration-color: #000080; font-weight: bold">Log hyperparameters</span></a> to attribute prompts and models to your test runs.

================================================================================
</pre>

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace">

<span style="color: #05f58d; text-decoration-color: #05f58d">✓</span> Evaluation completed 🎉! <span style="font-weight: bold">(</span>time taken: <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">7.</span>67s | token cost: <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">0.0009520000000000002</span> USD<span style="font-weight: bold">)</span>
» Test Results <span style="font-weight: bold">(</span><span style="color: #008080; text-decoration-color: #008080; font-weight: bold">1</span> total tests<span style="font-weight: bold">)</span>:
   » Pass Rate: <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">100.0</span>% | Passed: <span style="color: #008000; text-decoration-color: #008000; font-weight: bold">1</span> | Failed: <span style="color: #800000; text-decoration-color: #800000; font-weight: bold">0</span>

 ================================================================================ 

» Want to share evals with your team, or a place for your test cases to live? ❤️ 🏡
  » Run <span style="color: #008000; text-decoration-color: #008000; font-weight: bold">'deepeval view'</span> to analyze and save testing results on <span style="color: #6a00ff; text-decoration-color: #6a00ff">Confident AI</span>.


</pre>

<span style="font-size:18px;">Print G-Eval Results</span>

```python
# Print the score and reason
print(f"Extracted Score: {g_eval_result.test_results[0].metrics_data[0].score}")
print(f"Extracted Reason:")
print(textwrap.fill(g_eval_result.test_results[0].metrics_data[0].reason, width=100))

```

    Extracted Score: 0.8182425532696179
    Extracted Reason:
    The summary maintains a clear and logical flow, progressing from the negative test of the woman in
    Scotland to the confirmed Ebola case of Pauline Cafferkey, then to the hospital treatment and public
    health responses. It captures key points such as Cafferkey's travel, treatment, contact tracing, and
    government actions in a well-organized manner without abrupt jumps. The summary avoids redundancy
    and irrelevant details, though it omits some specifics like the involvement of Save the Children and
    the detailed description of the isolation unit, which slightly reduces completeness but does not
    harm coherence.

<span style="font-size:18px;">Inspect the CoT Automatically Generated by G-Eval</span>

```python
# Access the verbose logs attribute
cot_logs = g_eval_result.test_results[0].metrics_data[0].verbose_logs

# Print the logs
print("--- Extracted Chain of Thought (CoT) Logs ---")
print(cot_logs)
```

    --- Extracted Chain of Thought (CoT) Logs ---
    Criteria:
    The summary must be well-structured and well-organized, building from sentence to sentence to a coherent body of information.

    Evaluation Steps:
    [
        "Compare the Input and Actual Output to ensure the summary logically progresses from one sentence to the next, maintaining a clear and coherent flow.",
        "Check that the Actual Output captures the key points of the Input in a well-organized manner without abrupt jumps or disjointed information.",
        "Verify that each sentence in the Actual Output builds upon the previous one, creating a structured and unified summary reflecting the Input content.",
        "Assess whether the summary avoids redundancy and irrelevant details, focusing on a concise and coherent representation of the Input."
    ]

    Rubric:
    None

    Score: 0.8182425532696179

<span style="font-size:18px;">Run DAG Eval</span>

```python
from deepeval.test_case import LLMTestCaseParams, LLMTestCase
from deepeval.metrics import GEval, DAGMetric
#from deepeval.dag import DeepAcyclicGraph
from deepeval.metrics.dag import DeepAcyclicGraph, BaseNode, VerdictNode
from typing import Optional, List, Union
```

```python
test_case = LLMTestCase(
    input="""
Alice: "Today's agenda: product update, blockers, and marketing timeline. Bob, updates?"
Bob: "Core features are done, but we're optimizing performance for large datasets. Fixes by Friday, testing next week."
Alice: "Charlie, does this timeline work for marketing?"
Charlie: "We need finalized messaging by Monday."
Alice: "Bob, can we provide a stable version by then?"
Bob: "Yes, we'll share an early build."
Charlie: "Great, we'll start preparing assets."
Alice: "Plan: fixes by Friday, marketing prep Monday, sync next Wednesday. Thanks, everyone!"
""",
    actual_output="""
Intro:
Alice outlined the agenda: product updates, blockers, and marketing alignment.

Body:
Bob reported performance issues being optimized, with fixes expected by Friday. Charlie requested finalized messaging by Monday for marketing preparation. Bob confirmed an early stable build would be ready.

Conclusion:
The team aligned on next steps: engineering finalizing fixes, marketing preparing content, and a follow-up sync scheduled for Wednesday.
"""
)

```

```python

from deepeval.metrics.dag import (
    DeepAcyclicGraph,
    TaskNode,
    BinaryJudgementNode,
    NonBinaryJudgementNode,
    VerdictNode,
)

correct_order_node = NonBinaryJudgementNode(
    criteria="Are the summary headings in the correct order: 'intro' => 'body' => 'conclusion'?",
    children=[
        VerdictNode(verdict="Yes", score=10),
        VerdictNode(verdict="Two are out of order", score=4),
        VerdictNode(verdict="All out of order", score=2),
    ],
)

correct_headings_node = BinaryJudgementNode(
    criteria="Does the summary headings contain all three: 'intro', 'body', and 'conclusion'?",
    children=[
        VerdictNode(verdict=False, score=0),
        VerdictNode(verdict=True, child=correct_order_node),
    ],
)

extract_headings_node = TaskNode(
    instructions="Extract all headings in `actual_output`",
    evaluation_params=[LLMTestCaseParams.ACTUAL_OUTPUT],
    output_label="Summary headings",
    children=[correct_headings_node, correct_order_node],
)

# create the DAG
dag = DeepAcyclicGraph(root_nodes=[extract_headings_node])
```

```python
format_correctness = DAGMetric(name="Format Correctness", dag=dag)
format_correctness.measure(test_case)
```

    Output()

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace"></pre>

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace">
</pre>

    1.0

```python
print(format_correctness.score)
print(textwrap.fill(format_correctness.reason, width=100))
```

    1.0
    The score for Format Correctness [DAG] is 1.0 because, according to the DAG traversal, all required
    summary headings ('Intro:', 'Body:', 'Conclusion:') were present (BinaryJudgementNode) and in the
    correct order (NonBinaryJudgementNode), leading to a final deterministic verdict of 'Yes' at the
    VerdictNode.

```python
metric_g_eval = GEval(
    name="Format Correctness",
    evaluation_steps=[
        "The `actual_output` is completely wrong if it misses any of the headings: 'intro', 'body', 'conclusion'.",
        "If the `actual_output` has all the complete headings but are in the wrong order, penalize it.",
        "If the summary has all the correct headings and they are in the right order, give it a perfect score."
    ],
    evaluation_params=[LLMTestCaseParams.ACTUAL_OUTPUT]
)
```

```python
# Evaluate using G-Eval
print("--- Running G-Eval ---")
g_eval_result = evaluate([test_case], [metric_g_eval])
```

    --- Running G-Eval ---

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace">✨ You're running DeepEval's latest <span style="color: #6a00ff; text-decoration-color: #6a00ff">Format Correctness </span><span style="color: #6a00ff; text-decoration-color: #6a00ff; font-weight: bold">[</span><span style="color: #6a00ff; text-decoration-color: #6a00ff">GEval</span><span style="color: #6a00ff; text-decoration-color: #6a00ff; font-weight: bold">]</span><span style="color: #6a00ff; text-decoration-color: #6a00ff"> Metric</span>! <span style="color: #374151; text-decoration-color: #374151; font-weight: bold">(</span><span style="color: #374151; text-decoration-color: #374151">using gpt-</span><span style="color: #374151; text-decoration-color: #374151; font-weight: bold">4.1</span><span style="color: #374151; text-decoration-color: #374151">, </span><span style="color: #374151; text-decoration-color: #374151">strict</span><span style="color: #374151; text-decoration-color: #374151">=</span><span style="color: #374151; text-decoration-color: #374151; font-style: italic">False</span><span style="color: #374151; text-decoration-color: #374151">, </span>
<span style="color: #374151; text-decoration-color: #374151">async_mode</span><span style="color: #374151; text-decoration-color: #374151">=</span><span style="color: #374151; text-decoration-color: #374151; font-style: italic">True</span><span style="color: #374151; text-decoration-color: #374151; font-weight: bold">)</span><span style="color: #374151; text-decoration-color: #374151">...</span>
</pre>

    Output()

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace"></pre>

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace">
</pre>

    ======================================================================

    Metrics Summary

      - ✅ Format Correctness [GEval] (score: 1.0, threshold: 0.5, strict: False, evaluation model: gpt-4.1, reason: The actual output contains all required headings: 'intro', 'body', and 'conclusion', and they are presented in the correct order. Each section is clearly labeled and the content under each heading is relevant and complete, fully aligning with the evaluation steps., error: None)

    For test case:

      - input:
    Alice: "Today's agenda: product update, blockers, and marketing timeline. Bob, updates?"
    Bob: "Core features are done, but we're optimizing performance for large datasets. Fixes by Friday, testing next week."
    Alice: "Charlie, does this timeline work for marketing?"
    Charlie: "We need finalized messaging by Monday."
    Alice: "Bob, can we provide a stable version by then?"
    Bob: "Yes, we'll share an early build."
    Charlie: "Great, we'll start preparing assets."
    Alice: "Plan: fixes by Friday, marketing prep Monday, sync next Wednesday. Thanks, everyone!"

      - actual output:
    Intro:
    Alice outlined the agenda: product updates, blockers, and marketing alignment.

    Body:
    Bob reported performance issues being optimized, with fixes expected by Friday. Charlie requested finalized messaging by Monday for marketing preparation. Bob confirmed an early stable build would be ready.

    Conclusion:
    The team aligned on next steps: engineering finalizing fixes, marketing preparing content, and a follow-up sync scheduled for Wednesday.

      - expected output: None
      - context: None
      - retrieval context: None

    ======================================================================

    Overall Metric Pass Rates

    Format Correctness [GEval]: 100.00% pass rate

    ======================================================================

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace">
<span style="color: #808000; text-decoration-color: #808000; font-weight: bold">⚠ WARNING:</span> No hyperparameters logged.
» <a href="https://deepeval.com/docs/evaluation-prompts" target="_blank"><span style="color: #000080; text-decoration-color: #000080; font-weight: bold">Log hyperparameters</span></a> to attribute prompts and models to your test runs.

================================================================================
</pre>

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace">

<span style="color: #05f58d; text-decoration-color: #05f58d">✓</span> Evaluation completed 🎉! <span style="font-weight: bold">(</span>time taken: <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">1.</span>64s | token cost: <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">0.001272</span> USD<span style="font-weight: bold">)</span>
» Test Results <span style="font-weight: bold">(</span><span style="color: #008080; text-decoration-color: #008080; font-weight: bold">1</span> total tests<span style="font-weight: bold">)</span>:
   » Pass Rate: <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">100.0</span>% | Passed: <span style="color: #008000; text-decoration-color: #008000; font-weight: bold">1</span> | Failed: <span style="color: #800000; text-decoration-color: #800000; font-weight: bold">0</span>

 ================================================================================ 

» Want to share evals with your team, or a place for your test cases to live? ❤️ 🏡
  » Run <span style="color: #008000; text-decoration-color: #008000; font-weight: bold">'deepeval view'</span> to analyze and save testing results on <span style="color: #6a00ff; text-decoration-color: #6a00ff">Confident AI</span>.


</pre>

```python
# Print the score and reason
print(f"Extracted Score: {g_eval_result.test_results[0].metrics_data[0].score}")
print(f"Extracted Reason:")
print(textwrap.fill(g_eval_result.test_results[0].metrics_data[0].reason, width=100))
```

    Extracted Score: 1.0
    Extracted Reason:
    The actual output contains all required headings: 'intro', 'body', and 'conclusion', and they are
    presented in the correct order. Each section is clearly labeled and the content under each heading
    is relevant and complete, fully aligning with the evaluation steps.

## What is Coming Up in Session 3

<span style="font-size:20px;">Two important practical use cases</span>

- <span style="font-size:18px;">RAG Evaluation End-to-End</span>
- <span style="font-size:18px;">Agent Evaluation End-to-End</span>
