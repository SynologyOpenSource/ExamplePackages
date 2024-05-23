module.exports = {
    root: true,
    globals: {
        __STRINGS__: true,
    },
    parserOptions: {
        parser: "@babel/eslint-parser",
        sourceType: 'module',
		babelOptions: {
			rootMode: 'upward',
		}
    },
    env: {
        browser: true,
    },
	extends: ['plugin:vue/base', '/.eslintrc.json'],
    // required to lint *.vue files
    plugins: [
        'vue'
    ],
    // add your custom rules here
    'rules': {
        "no-unused-vars": ["error", {
            "vars": "all",
            "args": "none"
        }],
        'no-debugger': process.env.NODE_ENV === 'production' ? 2 : 0,
        "no-console": 1,
    }
}
