/***************************************************************************
 * string_pool.cc -- String interning for memory optimization              *
 ***********************IMPORTANT NMAP LICENSE TERMS************************
 *                                                                         *
 * The Nmap Security Scanner is (C) 1996-2020 Insecure.Com LLC ("The Nmap  *
 * Project"). Nmap is also a registered trademark of the Nmap Project.     *
 *                                                                         *
 * This program is distributed under the terms of the Nmap Public Source   *
 * License (NPSL). The exact license text applying to a particular Nmap    *
 * release or source code control revision is contained in the LICENSE     *
 * file distributed with that version of Nmap or source code control       *
 * revision. More Nmap copyright/legal information is available from       *
 * https://nmap.org/book/man-legal.html, and further information on the    *
 * NPSL license itself can be found at https://nmap.org/npsl. This header  *
 * summarizes some key points from the Nmap license, but is no substitute  *
 * for the actual license text.                                            *
 *                                                                         *
 * Nmap is generally free for end users to download and use themselves,    *
 * including commercial use. It is available from https://nmap.org.        *
 *                                                                         *
 * The Nmap license generally prohibits companies from using and           *
 * redistributing Nmap in commercial products, but we sell a special Nmap  *
 * OEM Edition with a more permissive license and special features for     *
 * this purpose. See https://nmap.org/oem                                  *
 *                                                                         *
 * If you have received a written Nmap license agreement or contract       *
 * stating terms other than these (such as an Nmap OEM license), you may   *
 * choose to use and redistribute Nmap under those terms instead.          *
 *                                                                         *
 * The official Nmap Windows builds include the Npcap software             *
 * (https://npcap.org) for packet capture and transmission. It is under    *
 * separate license terms which forbid redistribution without special      *
 * permission. So the official Nmap Windows builds may not be              *
 * redistributed without special permission (such as an Nmap OEM           *
 * license).                                                               *
 *                                                                         *
 * Source is provided to this software because we believe users have a     *
 * right to know exactly what a program is going to do before they run it. *
 * This also allows you to audit the software for security holes.          *
 *                                                                         *
 * Source code also allows you to port Nmap to new platforms, fix bugs,    *
 * and add new features.  You are highly encouraged to submit your         *
 * changes as a Github PR or by email to the dev@nmap.org mailing list     *
 * for possible incorporation into the main distribution. Unless you       *
 * specify otherwise, it is understood that you are offering us very       *
 * broad rights to use your submissions as described in the Nmap Public    *
 * Source License Contributor Agreement. This is important because we      *
 * fund the project by selling licenses with various terms, and also       *
 * because the inability to relicense code has caused devastating          *
 * problems for other Free Software projects (such as KDE and NASM).       *
 *                                                                         *
 * The free version of Nmap is distributed in the hope that it will be     *
 * useful, but WITHOUT ANY WARRANTY; without even the implied warranty of  *
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. Warranties,        *
 * indemnification and commercial support are all available through the    *
 * Npcap OEM program--see https://nmap.org/oem.                            *
 *                                                                         *
 ***************************************************************************/
#include "string_pool.h"
#include <nbase.h>

#include <set>
#include <string>
#include <utility>
#include <stdarg.h>
#include <ctype.h>

/* Keep assert() defined for security reasons */
#undef NDEBUG
#include <assert.h>

const char *string_pool_insert(const char *s)
{
  static std::set<std::string> pool;
  static std::pair<std::set<std::string>::iterator, bool> pair;

  pair = pool.insert(s);

  return pair.first->c_str();
}

const char *string_pool_substr(const char *s, const char *t)
{
  return string_pool_insert(std::string(s, t).c_str());
}

const char *string_pool_substr_strip(const char *s, const char *t) {
  while (isspace((int) (unsigned char) *s))
    s++;
  while (t > s && isspace((int) (unsigned char) *(t - 1)))
    t--;

  return string_pool_substr(s, t);
}

const char *string_pool_strip_word(const char *s) {
  const char *t;

  while (isspace((int) (unsigned char) *s))
    s++;
  t = s;
  while (*t != '\0' && !isspace((int) (unsigned char) *t))
    t++;

  if (s == t)
    return NULL;

  return string_pool_substr(s, t);
}

/* Format a string with sprintf and insert it with string_pool_insert. */
const char *string_pool_sprintf(const char *fmt, ...)
{
  const char *s;
  char *buf;
  int size, n;
  va_list ap;

  buf = NULL;
  size = 32;
  /* Loop until we allocate a string big enough for the sprintf. */
  for (;;) {
    buf = (char *) realloc(buf, size);
    assert(buf != NULL);
    va_start(ap, fmt);
    n = Vsnprintf(buf, size, fmt, ap);
    va_end(ap);
    if (n < 0)
      size = size * 2;
    else if (n >= size)
      size = n + 1;
    else
      break;
  }

  s = string_pool_insert(buf);
  free(buf);

  return s;
}
