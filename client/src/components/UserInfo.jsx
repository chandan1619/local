import { useSelector } from "react-redux";

const UserInfo = () => {
  const user = useSelector((state) => state.user.value);
  return (
    <div className="bg-slate-300 shadow-lg rounded px-8 pt-6 pb-8 mb-4 w-96">
      <div className="mb-6">
        <label
          className="block text-gray-700 text-sm font-bold mb-2"
          htmlFor="email"
        >
          Name
        </label>
        <input
          className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
          id="email"
          type="email"
          value={user?.name}
          placeholder="Email Address"
        />
      </div>
      <div className="mb-6">
        <label
          className="block text-gray-700 text-sm font-bold mb-2"
          htmlFor="email"
        >
          Email Address
        </label>
        <input
          className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
          id="email"
          type="email"
          value={user?.email}
          placeholder="Email Address"
          disabled
        />
      </div>
    </div>
  );
};

export default UserInfo;
