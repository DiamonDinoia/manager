import test from "node:test";
import assert from "node:assert/strict";
import managerExtension, { managerInstructions } from "../index.js";

function makePi() {
  const commands = {};
  const handlers = {};
  return {
    registerCommand: (name, cfg) => { commands[name] = cfg; },
    on: (event, handler) => { (handlers[event] ||= []).push(handler); },
    sendUserMessage: () => {},
    commands,
    handlers,
  };
}

test("loads instructions from the skill body", () => {
  assert.match(managerInstructions(), /Context budget \(hard rules\)/);
});

test("injects instructions only while active", async () => {
  const pi = makePi();
  managerExtension(pi);
  const before = pi.handlers.before_agent_start[0];
  assert.equal(await before({ systemPrompt: "base" }), undefined);
  await pi.commands.manager.handler("fix the flaky test", { ui: { notify: () => {} } });
  const out = await before({ systemPrompt: "base" });
  assert.match(out.systemPrompt, /^base\n\n/);
  assert.match(out.systemPrompt, /Dispatch tiers/);
});

test("stop manager deactivates", async () => {
  const pi = makePi();
  managerExtension(pi);
  const before = pi.handlers.before_agent_start[0];
  await pi.commands.manager.handler("", { ui: { notify: () => {} } });
  assert.ok(await before({ systemPrompt: "base" }));
  await pi.handlers.input[0]({ text: "stop manager" });
  assert.equal(await before({ systemPrompt: "base" }), undefined);
});
