const path = require('path');
const fs = require('fs');
const solc = require('solc');

const inboxPath = path.resolve(__dirname, 'contracts', 'Inbox.sol');
const source = fs.readFileSync(inboxPath, 'utf8');

const input = {
  language: 'Solidity',
  sources: {
    'Inbox.sol': {
      content: source,
    },
  },
  settings: {
    outputSelection: {
      '*': {
        '*': ['abi', 'evm.bytecode'],
      },
    },
  },
};

const compiled = JSON.parse(solc.compile(JSON.stringify(input)));
const output = compiled.contracts['Inbox.sol'].Inbox;

// melihat hasil kompilasi
console.log("ABI:", JSON.stringify(output.abi, null, 2));
console.log("Bytecode:", output.evm.bytecode.object.slice(0, 60), "...");

module.exports = output;
