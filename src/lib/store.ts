import { create } from 'zustand';
type State={repoPath:string; activeRepo?:string; setRepoPath:(path:string)=>void; setActiveRepo:(repo:string)=>void};
export const useAppStore=create<State>((set)=>({repoPath:'.',setRepoPath:(repoPath)=>set({repoPath}),setActiveRepo:(activeRepo)=>set({activeRepo})}));
