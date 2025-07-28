import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion";

const steps = [
  {
    id: 1,
    title: "Bootstrap Script Deployment",
    content: "Generate and deploy the initial PLUTO-JACKAL bootstrap script to the VPS.",
    mandatory: true,
    help: "This script sets up the core agent logic. It must be deployed and confirmed before continuing."
  },
  {
    id: 2,
    title: "Codex GitOps Manager",
    content: "Build Codex GitHub Manager to automate Git pushes and deployment workflows.",
    mandatory: true,
    help: "This step enables PLUTO-JACKAL to update its code autonomously."
  },
  {
    id: 3,
    title: "Runtime Debugging Harness",
    content: "Set up an environment for agents to test and debug their own code with safety nets.",
    mandatory: false,
    help: "While not required immediately, this ensures generated code is validated before live deployment."
  },
  {
    id: 4,
    title: "Litellm Gateway",
    content: "Deploy a model routing gateway to handle multiple LLMs.",
    mandatory: false,
    help: "Provides flexible AI routing to ensure resilience and scalability."
  }
];

export default function PlutoJackalDashboard() {
  const [stepIndex, setStepIndex] = useState(0);
  const [completedSteps, setCompletedSteps] = useState([]);

  const currentStep = steps[stepIndex];

  const handleNext = () => {
    if (currentStep.mandatory && !completedSteps.includes(currentStep.id)) {
      alert("You must complete this step before proceeding.");
      return;
    }
    setStepIndex((prev) => Math.min(prev + 1, steps.length - 1));
  };

  const handlePrev = () => {
    setStepIndex((prev) => Math.max(prev - 1, 0));
  };

  const markComplete = () => {
    if (!completedSteps.includes(currentStep.id)) {
      setCompletedSteps([...completedSteps, currentStep.id]);
    }
  };

  return (
    <div className="p-6 space-y-6">
      <Card>
        <CardContent className="space-y-4">
          <h2 className="text-xl font-bold">Step {currentStep.id}: {currentStep.title}</h2>
          <p>{currentStep.content}</p>
          <Button onClick={markComplete} disabled={completedSteps.includes(currentStep.id)}>
            {completedSteps.includes(currentStep.id) ? "✅ Completed" : "Mark Step Complete"}
          </Button>

          <Accordion type="single" collapsible>
            <AccordionItem value="help">
              <AccordionTrigger>Need Help?</AccordionTrigger>
              <AccordionContent>
                {currentStep.help}
              </AccordionContent>
            </AccordionItem>
          </Accordion>

          <div className="flex justify-between pt-6">
            <Button onClick={handlePrev} disabled={stepIndex === 0}>Previous</Button>
            <Button onClick={handleNext} disabled={stepIndex === steps.length - 1}>Next</Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
