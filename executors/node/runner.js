const input = process.env.INPUT || '';
const code = process.env.CODE || '';

if (input) {
    process.stdin.push(input);
}

try {
    eval(code);
} catch (e) {
    console.error(`Error: ${e.message}`);
    process.exit(1);
}