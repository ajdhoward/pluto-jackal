import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";

// Quick setup wizard with integrated download buttons, commands, and API validation
const quickSteps = [
  {
    id: 1,
    title: "Run Bootstrap Script",
    action: (
      <>
        <Button asChild>
          <a href="/downloads/pluto_jackal_bootstrap.sh" download>⬇️ Download Bootstrap Script</a>
        </Button>
        <p className="mt-2 text-sm text-muted-foreground">Upload to `/root/` in Cockpit or SCP and run:</p>
        <pre className="bg-muted p-2 rounded text-sm">bash pluto_jackal_bootstrap.sh</pre>
      </>
    ),
    help: "This script sets up PLUTO-JACKAL's base environment and agent logic."
  },
  {
    id: 2,
    title: "Connect GitHub",
    action: (
      <>
        <Input placeholder="Paste GitHub PAT here" />
        <Button variant="secondary" className="mt-2">Validate & Link Repo</Button>
        <pre className="bg-muted p-2 rounded text-sm mt-2">export GITHUB_PAT=your-token</pre>
      </>
    ),
    help: "Links PLUTO-JACKAL to your GitHub repo for autonomous commits and deployments."
  },
  {
    id: 3,
    title: "Enter AI Model Hub Credentials",
    action: (
      <>
        <Input placeholder="Token ID" id="tokenId" />
        <Input placeholder="Token Value" id="tokenValue" className="mt-2" />
        <Button
          variant="secondary"
          className="mt-2"
          onClick={() => {
            const id = document.getElementById("tokenId").value;
            const value = document.getElementById("tokenValue").value;
            if (!id || !value) {
              alert("Please enter both Token ID and Token Value.");
              return;
            }
            // Simulate API validation using Basic Auth or proper header structure
            fetch("https://api.ionos.com/ai/v1/status", {
              headers: { Authorization: `Basic ${btoa(id + ":" + value)}` }
            })
              .then((res) => {
                if (res.ok) {
                  alert("✅ API Credentials validated successfully!");
                } else {
                  alert("❌ Invalid credentials or connection error.");
                }
              })
              .catch(() => alert("❌ Unable to reach AI Model Hub API."));
          }}
        >
          Test AI Hub Connection
        </Button>
        <pre className="bg-muted p-2 rounded text-sm mt-2">export AI_HUB_ID=your-id\nexport AI_HUB_KEY=your-key</pre>
      </>
    ),
    help: "Connects PLUTO-JACKAL to IONOS AI Model Hub SDK for LLM orchestration, validating credentials live."
  },
  {
    id: 4,
    title: "Start Autonomous Agent",
    action: (
      <>
        <Button variant="default" className="mt-2">🚀 Launch Coding Agent</Button>
        <pre className="bg-muted p-2 rounded text-sm mt-2">systemctl start pluto-jackal-agent</pre>
      </>
    ),
    help: "Starts PLUTO-JACKAL’s AI agent to autonomously code, validate, and push updates."
  }
];

export default function QuickStartPlutoJackal() {
  const [stepIndex, setStepIndex] = useState(0);
  const [completed, setCompleted] = useState([]);

  const current = quickSteps[stepIndex];

  const completeStep = () => {
    if (!completed.includes(current.id)) setCompleted([...completed, current.id]);
  };

  return (
    <div className="p-6 space-y-6">
      <Card>
        <CardContent className="space-y-4">
          <h2 className="text-xl font-bold">Quick Setup – Step {current.id}: {current.title}</h2>
          <div>{current.action}</div>

          <Button onClick={completeStep}>
            {completed.includes(current.id) ? "✅ Done" : "Mark Step Done"}
          </Button>

          <details className="mt-4">
            <summary className="cursor-pointer font-medium">Need Help?</summary>
            <p className="mt-2 text-sm text-muted-foreground">{current.help}</p>
          </details>

          <div className="flex justify-between pt-6">
            <Button onClick={() => setStepIndex(Math.max(stepIndex - 1, 0))} disabled={stepIndex === 0}>Previous</Button>
            <Button onClick={() => setStepIndex(Math.min(stepIndex + 1, quickSteps.length - 1))} disabled={stepIndex === quickSteps.length - 1}>Next</Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
