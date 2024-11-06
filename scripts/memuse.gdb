define p_mctx
  printf "%p %-12s: inuse=%10lu maxinuse=%10lu quota=%lu poolcnt=%3u flags=%x\n", $arg0, $arg0->name, $arg0->inuse, $arg0->maxinuse, $arg0->quota, $arg0->poolcnt, $arg0->flags
end

document p_mctx
  Print one isc__mem structure in one line
end

define p_list_mctx
  if $argc > 0
    set $i = $arg0->head
  else
    set $i = contexts->head
  end
  set $index = 0
  set $total_inuse = 0lu
  set $total_maxinuse = 0lu
  while ($i)
    if ($i->inuse > 0)
      printf "[%3d] ", $index
      p_mctx $i
    end
    set $total_inuse += $i->inuse
    set $total_maxinuse += $i->maxinuse
    set $index++
    set $i = $i->link.next
  end
  printf "#Totals inuse=%10lu maxinuse=%10lu\n", $total_inuse, $total_maxinuse
end

document p_list_mctx
  Print LIST(isc_mem). contexts variable if not specified.
end
