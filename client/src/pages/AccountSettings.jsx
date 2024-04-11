import Header from "../components/Header";
import UserInfo from "../components/UserInfo";
const AccountSettings = () => {
  return (
    <div className="flex flex-col gap-y-16">
      <Header />
      <div className="flex justify-center items-center">
        <UserInfo />
      </div>
    </div>
  );
};

export default AccountSettings;
