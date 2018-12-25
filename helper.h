#include <string>
#include <iterator>
#include <iostream>
#include <ctype.h>
#include <sstream>
using namespace std;

template <class ForwardIterator, class OutputIterator, class UnaryPredicate>
void trim (
  ForwardIterator first, ForwardIterator last, OutputIterator result,
    UnaryPredicate pred
    )
{
  while (first != last && pred(*first))
  {
    first++;
  }

  for (ForwardIterator p = last; first != last; first++)
  {
    if (pred(*first))
    {
      p = first;
    }
    else
    {
      if (p != last)
      {
        *result = *p;
        p = last;
      }
      *result = *first;
    }
  }
}

inline bool isJunk(char c)
{
  return isspace(c);
}

inline string trim_string(string s)
{
  ostringstream result;
  trim(s.begin(), s.end(), ostream_iterator<char>(result, ""), isJunk);
  return  result.str();
}
