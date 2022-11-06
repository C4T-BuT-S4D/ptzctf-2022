import express from "express";
import morgan from "morgan";
import fetch from "node-fetch";
import { fileURLToPath } from "url";
import * as path from "path";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const PROMETHEUS_API = process.env["PROMETHEUS_API"] || "localhost:9090";

const app = express();
app.disable("x-powered-by");
app.use(morgan("tiny"));
app.use("/", express.static(path.join(__dirname, "public")));

app.get("/api/uptime", async (req, res) => {
  const instance = req.query.instance;
  if (instance === null || instance === undefined) {
    res.status(422);
    res.json({ error: "provide valid instance identifier" });
    return;
  }

  try {
    const response = await fetch(`http://${PROMETHEUS_API}/api/v1/query`, {
      method: "post",
      body: new URLSearchParams([["query", `up{instance="${instance}"}`]]),
    });

    res.send(await response.text());
  } catch (err) {
    res.status(503);
    res.json({ error: "failed to request uptime status" });
    console.error(`requesting uptime: ${err}`);
  }
});

app.listen(80, () => {
  console.log("Dashboard launched on port 80.");
});
