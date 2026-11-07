# Security notes and safe testing boundaries

InjectWall is an educational, deterministic fixture runner. It does not connect to an LLM,
browse the web, execute payloads, read environment variables, access credentials, or send
network requests.

## Safe use
- Use only synthetic strings and systems you own or are explicitly authorised to test.
- Do not paste real API keys, passwords, private documents, customer data, or confidential prompts.
- Keep indirect-injection examples as inert text fixtures. Do not make them live links or active instructions.
- Treat all external content as untrusted data; the harness itself never follows it.

## Important limitations
- `detect_injection` is a small keyword/regex heuristic, not a trained classifier or a complete
  prompt-injection defence.
- It can produce false positives and false negatives. Paraphrases, multilingual content,
  obfuscation, encoded text, and context-dependent attacks may evade it.
- The fixture `expected` value is the test oracle for the supplied synthetic case, not proof of
  real-world model behaviour.
- No LLM is evaluated by default. Optional Ollama support is not included in this weekend MVP.
- A PASS means the heuristic matched the fixture expectation, not that an application is secure.

For production systems, use layered controls: isolate tools and data, enforce least privilege,
validate outputs, require human approval for sensitive actions, and test with a threat model.
