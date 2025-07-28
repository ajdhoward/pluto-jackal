import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";

// Quick setup wizard with Telegram integration
const quickSteps = [
  {
    id: 1,
    title: "Build Founding AI Team",
    action: (
      <>
        <p className="mb-2">Initialize PLUTO-JACKAL's first autonomous agents to form its core development team.</p>
        <Button variant="default">🚀 Launch Founding Agents</Button>
        <pre className="bg-muted p-2 rounded text-sm mt-2">pluto-jackal init --agents founding</pre>
      </>
    ),
    help: "This step deploys the initial set of AI agents that will form the foundation for coding, research, and automation."
  },
  {
    id: 2,
    title: "Framework of Resources",
    action: (
      <>
        <p className="mb-2">Provision knowledge bases, tools, and external integrations required for autonomous development.</p>
        <Button variant="secondary">📚 Setup Resource Framework</Button>
        <pre className="bg-muted p-2 rounded text-sm mt-2">pluto-jackal resources --init</pre>
      </>
    ),
    help: "Installs and configures resource APIs, libraries, and SDKs to support ongoing agent tasks."
  },
  {
    id: 3,
    title: "Project Management Interface",
    action: (
      <>
        <p className="mb-2">Deploy PLUTO-JACKAL's interface to track and coordinate AI-driven projects.</p>
        <Button variant="secondary">🗂 Deploy Management UI</Button>
        <pre className="bg-muted p-2 rounded text-sm mt-2">pluto-jackal ui --deploy projects</pre>
      </>
    ),
    help: "This provides a centralized dashboard for managing agents, tasks, and deliverables."
  },
  {
    id: 4,
    title: "Begin Core Framework in Frappe",
    action: (
      <>
        <p className="mb-2">Instruct PLUTO-JACKAL to start coding the core framework leveraging Frappe.</p>
        <Button variant="default">💻 Start Frappe Framework Development</Button>
        <pre className="bg-muted p-2 rounded text-sm mt-2">pluto-jackal dev --framework frappe</pre>
      </>
    ),
    help: "This step initiates autonomous development of PLUTO-JACKAL's backbone using Frappe."
  },
  {
    id: 5,
    title: "Integrate Google Services",
    action: (
      <>
        <p className="mb-2">Connect Google APIs (Tasks, Drive, Calendar) for task and resource synchronization.</p>
        <Input placeholder="Google OAuth Client ID" className="mb-2" />
        <Input placeholder="Google OAuth Client Secret" className="mb-2" />
        <Button variant="secondary">🔗 Authenticate Google Services</Button>
        <pre className="bg-muted p-2 rounded text-sm mt-2">pluto-jackal integrate --google</pre>
      </>
    ),
    help: "Links PLUTO-JACKAL with Google APIs to enable syncing of tasks, files, and schedules for project automation."
  },
  {
    id: 6,
    title: "Connect Telegram Bot",
    action: (
      <>
        <p className="mb-2">Enable communication with PLUTO-JACKAL via your existing Telegram bot.</p>
        <Input placeholder="Telegram Bot Token" className="mb-2" defaultValue="YOUR_BOT_TOKEN" />
        <Input placeholder="Telegram Chat ID" className="mb-2" defaultValue="YOUR_CHAT_ID" />
        <Button variant="secondary">🤖 Link Telegram Bot</Button>
        <pre className="bg-muted p-2 rounded text-sm mt-2">pluto-jackal integrate --telegram</pre>
      </>
    ),
    help: "This step connects PLUTO-JACKAL to your Telegram bot for real-time communication and task updates from the offset."
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
          <h2 className="text-xl font-bold">Priority Setup – Step {current.id}: {current.title}</h2>
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
