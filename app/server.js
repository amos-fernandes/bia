const path = require('path');
const { logger: rootLogger, mongo } = require('./helpers');
const { runBinance } = require('./server-binance');
const { runCronjob } = require('./server-cronjob');
const { runFrontend } = require('./server-frontend');
const { runErrorHandler } = require('./error-handler');

global.appRoot = path.resolve(__dirname);

const express = require('express');
const app = express();
const PORT = process.env.PORT || 8080;

(async () => {
  const logger = rootLogger.child({
    gitHash: process.env.GIT_HASH || 'unspecified'
  });

  runErrorHandler(logger);

  await mongo.connect(logger);

  await Promise.all([
    runBinance(logger),
    runCronjob(logger),
    runFrontend(logger)
  ]);
})();
