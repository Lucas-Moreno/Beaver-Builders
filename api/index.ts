import bodyParser from "body-parser";
import cors from "cors";
import dotenv from "dotenv";
import express from "express";
import process from "process";
import router from "./src/routes/routes";
import { Express } from "./src/types/types";

dotenv.config();

const PORT = process.env.PORT_BACK;
const app: Express = express();

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

const corsOptions = {
  origin: ["http://localhost:4200"],
  credentials: true,
  optionsSuccessStatus: 200,
};

app.use(cors(corsOptions));

app.use("/", router);

app.listen(PORT);

module.exports = app;
