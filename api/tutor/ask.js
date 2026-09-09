import connectDB from "../../backend/lib/db.js";
import Document from "../../backend/models/Document.js";
import { requireAuth } from "../../backend/lib/auth.js";
import { generateText } from "../../backend/lib/local-ai.js";
import {
  createOfflineTutorAnswer,
  offlineFallbackEnabled,
} from "../../backend/lib/offline-ai.js";
import { sendError, setCors } from "../_utils.js";

export default async function handler(req,res){
  setCors(res, req);
  if (req.method === "OPTIONS") return res.status(204).end();
  try{
    if(req.method!=="POST")return res.status(405).json({message:"Method not allowed"});
    const {userId}=requireAuth(req); await connectDB();
    const {documentId,question}=req.body||{};
    if(!question?.trim())return res.status(400).json({message:"Question is required"});
    const doc=await Document.findOne({_id:documentId,userId});
    if(!doc)return res.status(404).json({message:"Material not found"});
    let answer;
    let offline = false;
    try {
      answer=await generateText(`You are a college teacher. Answer the student's question using ONLY the uploaded material below. If the material does not contain enough information, clearly say so. Explain simply and give an example when supported. Student question: ${question}\\n\\nUploaded material:\\n${doc.extractedText.slice(0,60000)}`);
    } catch (error) {
      if (!offlineFallbackEnabled()) throw error;
      offline = true;
      answer = createOfflineTutorAnswer(question, doc.extractedText);
    }
    return res.json({
      answer,
      ...(offline
        ? {
            warning:
              "Ollama was unavailable, so an excerpt-based offline answer was returned.",
          }
        : {}),
    });
  }catch(e){return sendError(res,e);}
}