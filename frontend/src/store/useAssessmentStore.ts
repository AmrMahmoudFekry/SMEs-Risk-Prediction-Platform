import { create } from 'zustand';

interface AssessmentState {
  step: number;
  smeData: Record<string, any>;
  isProcessing: boolean;
  setStep: (step: number) => void;
  updateSmeData: (data: Record<string, any>) => void;
  setProcessing: (status: boolean) => void;
  resetForm: () => void;
}

export const useAssessmentStore = create<AssessmentState>((set) => ({
  step: 1,
  smeData: {},
  isProcessing: false,
  
  setStep: (step) => set({ step }),
  
  updateSmeData: (data) => set((state) => ({ 
    smeData: { ...state.smeData, ...data } 
  })),
  
  setProcessing: (status) => set({ isProcessing: status }),
  
  resetForm: () => set({ step: 1, smeData: {}, isProcessing: false })
}));