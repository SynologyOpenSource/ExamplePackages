const path = require('path');
const fs = require('fs');
const webpack = require('webpack');
const VueLoaderPlugin = require('vue-loader/lib/plugin');
const ESLintPlugin = require('eslint-webpack-plugin');
const STRING_PATH = '/source/uistring/MariaDB';
const { getString } = require('/source/synopkgutils/string.js');

// Retrive the strings from the uistring folder
const stringsEntries = [
	['wizard', 'port'],
	['wizard', 'wizard_set_data_title'],
	['ui', 'db_new_password'],
	['ui', 'db_confirm_password'],
	['mariadb10', 'invalid_user_password_2'],
];

function resolve (dir) {
	return path.join(__dirname, dir)
}

async function traverseStringPath() {
	const texts = {};
	fs.readdirSync(STRING_PATH).forEach(dir => {
		const lang = path.basename(dir);
		const langStringFile = `${STRING_PATH}/${lang}/strings`;
		texts[lang] = {};
		for (const [section, key] of stringsEntries) {
			texts[lang][section] = texts[lang][section] ?? {};
			texts[lang][section][key] = getString(langStringFile, section, key).replace('@PKG_NAME@', 'MariaDB');
		}
	});
	return texts;
}

module.exports = async (env, argv) => {
	const isDevelopment = argv.mode === 'development';
	return {
		mode: isDevelopment ? 'development' : 'production',
		devtool: isDevelopment ? 'inline-source-map' : false,
		module: {
			rules: [
				{
					test: /\.vue$/,
					loader: 'vue-loader'
				},
				{
					exclude: /node_modules/,
					test: /\.js$/,
					use: {
						loader: 'babel-loader',
						options: {
							rootMode: 'upward'
						}
					}
				},
			]
		},
		resolve: {
			extensions: ['.js', '.vue', '.json'],
		},
		entry: {
			// uninstall entry
			remove_entry: './src/remove-entry.js',
			remove_notice_entry: './src/remove-notice-entry.js',
			// install entry
			install_entry: './src/install-entry.js',
		},
		output: {
			library: {
				name: 'SYNO.SDS.PkgManApp.Custom.JsonpLoader.load',
				type: 'jsonp',
			},
			path: resolve('dist'),
			filename: '[name].bundle.js'
		},
		plugins: [
			new VueLoaderPlugin(),
			new ESLintPlugin({ extensions: ['js', 'ts', 'vue'] }),
			new webpack.DefinePlugin({
				__STRINGS__: JSON.stringify(await traverseStringPath())
			}),
		],
		externalsType: 'window',
		externals: {
			'vue': 'Vue',
		},
		watchOptions: {
			poll: true,
		},
	};
}
