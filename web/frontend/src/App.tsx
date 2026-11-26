import { Navigate, Route, Routes } from "react-router-dom";

import SignUp from "./pages/SignUp";
import Login from "./pages/Login";
import Onboarding from "./pages/Onboarding";
import OnboardingAcademics from "./pages/OnboardingAcademics";
import OnboardingResults from "./pages/OnboardingResults";
import Home from "./pages/Home";
import Profile from "./pages/Profile";
import Recommendations from "./pages/Recommendations";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/signup" replace />} />

      <Route path="/signup" element={<SignUp />} />
      <Route path="/login" element={<Login />} />

      <Route path="/onboarding" element={<Onboarding />} />
      <Route path="/onboarding/academics" element={<OnboardingAcademics />}/>
      <Route path="/onboarding/results" element={<OnboardingResults />}/>
      <Route path="/home" element={<Home />} />
      <Route path="/recommendations" element={<Recommendations />}/>
      <Route path="/profile" element={<Profile />} />

      <Route path="*" element={<Navigate to="/signup" replace />} />
    </Routes>
  );
}

export default App;