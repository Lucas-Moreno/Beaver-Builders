import jsonData from "../../../IA/data.json";
import { Request, Response } from "../types/types";

export const getData = async (req: Request, res: Response) => {
  try {
    res.status(200).json({ jsonData });
  } catch (err) {
    console.error("Error fetching data:", err);
    res.status(500).json({ error: "Internal server error" });
  }
};