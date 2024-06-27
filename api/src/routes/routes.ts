import express, { Request, Response } from "express";
import {
  getData
} from "../controllers/data.controller";

import { Router } from "../types/types";

const router: Router = express.Router();

// Welcome to my api
router.get("/", (req: Request, res: Response) => {
  res.send("Welcome to my API");
});

// Data
router.get("/data", getData);

export default router;
