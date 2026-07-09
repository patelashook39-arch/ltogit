#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import math
import random
import json
import asyncio
from datetime import datetime

# --- CORE EMBEDDING CONSTANTS ---
V_DIM = 1536
L_CTX = 8192
TEMP = 0.7
ALPHA = 0.001
BETA = 0.99

# --- STREAMING OUTPUT STYLES ---
M_CLR = "\033[1;35m"
C_CLR = "\033[1;36m"
G_CLR = "\033[1;32m"
Y_CLR = "\033[1;33m"
R_CLR = "\033[1;31m"
W_CLR = "\033[1;37m"
RST = "\033[0m"

class Tokenizer:
    def __init__(self):
        self.vocab_size = 50257
        self.bos_token = 1
        self.eos_token = 2

    def encode(self, text):
        return [random.randint(100, 45000) for _ in range(min(len(text.split()), 12))]

    def decode(self, tokens):
        words = ["lambda", "tensor", "gradient", "weights", "matrix", "agent", "state", "policy", "reward", "action", "node", "entropy"]
        return " ".join(random.choice(words) for _ in tokens)

class VectorMemory:
    def __init__(self, dimension=V_DIM):
        self.dim = dimension
        self.nodes = {}
        self.index = []

    def commit(self, node_id, vector, metadata):
        self.nodes[node_id] = {"vector": vector, "meta": metadata, "timestamp": time.time()}
        self.index.append(node_id)
        magnitude = math.sqrt(sum(x*x for x in vector))
        sys.stdout.write(f"{M_CLR}[MEMORY_STORE] Node {node_id} committed. Magn: {magnitude:.4f}{RST}\n")
        sys.stdout.flush()

    def query_similarity(self, query_vector, top_k=3):
        results = []
        for n_id, data in self.nodes.items():
            v = data["vector"]
            dot_prod = sum(x*y for x, y in zip(query_vector, v))
            mag_q = math.sqrt(sum(x*x for x in query_vector))
            mag_v = math.sqrt(sum(x*x for x in v))
            score = dot_prod / (mag_q * mag_v) if (mag_q * mag_v) > 0 else 0
            results.append((n_id, score))
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_k]

class NeuralLayer:
    def __init__(self, in_features, out_features):
        self.in_f = in_features
        self.out_f = out_features
        self.weights = [[random.uniform(-0.1, 0.1) for _ in range(out_features)] for _ in range(in_features)]
        self.biases = [0.0] for _ in range(out_features)

    def forward(self, input_vector):
        output = []
        for j in range(self.out_f):
            activation = sum(input_vector[i] * self.weights[i][j] for i in range(self.in_f)) + self.biases[j]
            output.append(1.0 / (1.0 + math.exp(-max(-50.0, min(50.0, activation)))))
        return output

class CognitivePipeline:
    def __init__(self):
        self.tokenizer = Tokenizer()
        self.memory = VectorMemory()
        self.layer1 = NeuralLayer(64, 128)
        self.layer2 = NeuralLayer(128, 64)
        self.active_session = f"session_{random.randint(1000, 9999)}"

    def log_internal(self, component, message, color=C_CLR):
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        sys.stdout.write(f"{W_CLR}[{timestamp}] {color}[{component}] {message}{RST}\n")
        sys.stdout.flush()

    def generate_synthetic_vector(self):
        return [random.gauss(0, 1) for _ in range(V_DIM)]

    async def ingest_perception(self, raw_input):
        self.log_internal("PERCEPTION", f"Ingesting payload: '{raw_input[:40]}...'", C_CLR)
        await asyncio.sleep(0.4)
        tokens = self.tokenizer.encode(raw_input)
        self.log_internal("TOKENIZER", f"Encoded sequence mapping: {tokens}", Y_CLR)
        return tokens

    async def cross_reference_attention(self, tokens):
        self.log_internal("ATTENTION", "Calculating multi-head matrix products...", G_CLR)
        await asyncio.sleep(0.6)
        query_v = [random.uniform(-1, 1) for _ in range(64)]
        hidden_1 = self.layer1.forward(query_v)
        hidden_2 = self.layer2.forward(hidden_1)
        
        for idx in range(3):
            addr = f"0x{random.randint(0x1000, 0x9FFF):04X}"
            loss = random.uniform(0.01, 0.05)
            self.log_internal("BACKPROP", f"Step {idx+1}/3 -> Softmax weight decay applied at {addr} | Loss: {loss:.6f}", R_CLR)
            await asyncio.sleep(0.2)
        
        return hidden_2

    async def retrieve_knowledge_base(self):
        self.log_internal("KNOWLEDGE_RETRIEVAL", "Scanning distributed embedding shards...", M_CLR)
        await asyncio.sleep(0.5)
        mock_query = [random.uniform(-1, 1) for _ in range(V_DIM)]
        matches = self.memory.query_similarity(mock_query)
        self.log_internal("KNOWLEDGE_RETRIEVAL", f"Top match nodes returned: {matches}", M_CLR)

    async def execute_policy_loop(self, cycles=15):
        self.log_internal("POLICY_ENGINE", "Initializing agent workspace environment...", W_CLR)
        
        for k in range(3):
            v_id = f"node_delta_{random.randint(100,999)}"
            self.memory.commit(v_id, self.generate_synthetic_vector(), {"tag": "baseline_context"})
            await asyncio.sleep(0.1)

        for i in range(1, cycles + 1):
            sys.stdout.write("\n")
            self.log_internal("AGENT_LOOP", f"=== STARTING INFERENCE CYCLE {i}/{cycles} ===", W_CLR)
            
            raw_sample = f"System metadata update chunk sequence identifier {random.randint(10000,99999)}"
            tokens = await self.ingest_perception(raw_sample)
            
            attn_weights = await self.cross_reference_attention(tokens)
            entropy = -sum(p * math.log(p + 1e-9) for p in attn_weights[:10])
            self.log_internal("ATTENTION", f"Context entropy calculation: {entropy:.4f}", G_CLR)
            
            await self.retrieve_knowledge_base()
            
            self.log_internal("POLICY_ENGINE", "Sampling probabilistic action distribution from categorical logit tensor...", Y_CLR)
            await asyncio.sleep(0.4)
            
            chosen_action = random.choice(["EMIT_RESPONSE", "REFINE_INTERNAL_MODEL", "INDEX_KNOWLEDGE", "STANDBY"])
            confidence = random.uniform(0.85, 0.99)
            self.log_internal("DECISION_NODE", f"Selected primitive primitive: [{chosen_action}] with confidence parameter {confidence*100:.2f}%", G_CLR)
            
            if chosen_action == "EMIT_RESPONSE":
                decoded_output = self.tokenizer.decode(tokens)
                self.log_internal("OUTPUT_STREAM", f"Synthesized string: \"{decoded_output}\"", W_CLR)
            
            await asyncio.sleep(0.5)

async def main():
    pipeline = CognitivePipeline()
    await pipeline.execute_policy_loop(5)

if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
