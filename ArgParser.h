#include<iostream>
#include<map>
#include<string.h>
#include<cassert>

typedef std::map<std::string, std::string> Arguments;
typedef Arguments::iterator ArgumentsIter;

using namespace std;

class ArgParser {
    private:
    Arguments args;
    bool is_verbose;

    public:

    ArgParser(int argc, char ** argv, bool is_verbose=false){
      this->is_verbose = is_verbose;
      string last_arg = "";
      bool var_rcvd = true;
      // cout << "Parsing the command line arguments..." << endl;
      for(int argindex = 1; argindex < argc; argindex++)
      {
          // cout << "argindex " << argindex << ":    ";
          string token = argv[argindex];
          if (token.find("--") == 0)
          {
              if (var_rcvd == false)
              {
                   this->args[last_arg] = "true";
                   // cout << "true" << endl;
              }
              last_arg = token.substr(2);
              var_rcvd = false;
              // cout << token << endl;
          }
          else
          {
              if(var_rcvd ==true)
              {
                cout << "Missing argument name!" << endl;
                assert(false);
              }
              var_rcvd = true;
              this->args[last_arg] = token;
              // cout << " " << token << endl;
          }
      }

      if(var_rcvd == false)
      {
          this->args[last_arg] = "true";
      }

      if(this->is_verbose){
          cout << "---------------------------" << endl;
          cout << "Parsed arguments:" << endl;
          for(auto& a : this->args){
              cout << "    " << a.first << ": " << a.second << endl;
          }
          cout << "---------------------------" << endl;
      }
    }

    bool exists(string label){
      return (this->args.find(label) != this->args.end());
    }

    string getArg(string label, string defaultValue="None")
    {
        if(exists(label))
          return this->args[label];
        return defaultValue;
    }

    long getArgLong(string label, long defaultValue = -1)
    {
        if (this->is_verbose)
          // cout<< "Looking for a long value for argument" << label << endl;
        if(exists(label)){
          if (this->is_verbose)
            cout << label << ": " << this->args[label] << endl;
          return stol(this->args[label]);
        }
        else {
          if (this->is_verbose)
            cout << label << ": " << defaultValue << endl;
        }
        return defaultValue;
    }

    double getArgDouble(string label, double defaultValue = -1)
    {
        if(exists(label)){
          if (this->is_verbose)
            cout << label << ": " << this->args[label] << endl;
          return stod(this->args[label]);
        }
        else {
          if (this->is_verbose)
            cout << label << ": " << defaultValue << endl;
          return defaultValue;
        }
    }

    bool flagExists(string label)
    {
        return exists(label);
    }
};
