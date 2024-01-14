const rtf = new Intl.RelativeTimeFormat(undefined, { numeric: "auto" })

const PERIODS = [
  { subdiv: 60, name: "seconds" },
  { subdiv: 60, name: "minutes" },
  { subdiv: 24, name: "hours" },
  { subdiv: 7, name: "days" },
  { subdiv: 4.34524, name: "weeks" },
  { subdiv: 12, name: "months" },
  { subdiv: Number.POSITIVE_INFINITY, name: "years" },
]

export const formatRelativeTime = date => {
  let duration = (new Date(date) - new Date()) / 1000

  for (const period of PERIODS) {
    if (Math.abs(duration) < period.subdiv)
      return rtf.format(Math.round(duration), period.name)
    duration /= period.subdiv
  }
}

export const formatDatetime = date => new Date(date).toLocaleString()
